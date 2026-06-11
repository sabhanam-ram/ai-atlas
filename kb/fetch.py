"""Transcript acquisition: youtube-transcript-api first, Playwright as a
last-resort fallback. yt-dlp supplies video metadata. Writes the raw transcript
into references/youtube/<channel>/<id>.md (the provenance layer)."""
from __future__ import annotations

import datetime
import re
from typing import Optional

from . import config
from .slug import slugify

_YT_ID_RE = re.compile(r"(?:v=|/shorts/|/embed/|youtu\.be/|/live/)([A-Za-z0-9_-]{11})")


def extract_video_id(url: str) -> str:
    m = _YT_ID_RE.search(url)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url.strip()):
        return url.strip()
    raise ValueError(f"could not extract a YouTube video id from: {url!r}")


def _ts(seconds) -> str:
    seconds = int(float(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


# ------------------------------------------------------------------ metadata
def fetch_metadata(url: str) -> dict:
    """Best-effort metadata via yt-dlp (library). Returns a possibly-partial dict."""
    try:
        import yt_dlp  # noqa: WPS433
    except ImportError:
        print("  yt-dlp not installed; skipping metadata")
        return {}
    opts = {"quiet": True, "no_warnings": True, "skip_download": True, "noplaylist": True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:  # noqa: BLE001
        print(f"  yt-dlp metadata failed: {exc}")
        return {}
    upload = info.get("upload_date")  # YYYYMMDD
    pub = f"{upload[0:4]}-{upload[4:6]}-{upload[6:8]}" if upload and len(upload) == 8 else None
    name = info.get("uploader") or info.get("channel") or ""
    return {
        "title": info.get("title") or "",
        "channel_name": name,
        "channel_slug": slugify(name or info.get("channel_id") or "unknown"),
        "publish_date": pub,
        "duration_seconds": info.get("duration"),
        "language": (info.get("language") or "en"),
    }


# ------------------------------------------------------------------ transcript
def fetch_transcript_api(video_id: str, languages=("en", "en-US", "en-GB")) -> Optional[list]:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # noqa: WPS433
    except ImportError:
        return None
    langs = list(languages)
    try:
        try:  # youtube-transcript-api >= 1.0 (instance API)
            api = YouTubeTranscriptApi()
            fetched = api.fetch(video_id, languages=langs)
            raw = fetched.to_raw_data()
        except AttributeError:  # older classmethod API
            raw = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
        return [{"start": seg["start"], "text": " ".join(seg["text"].split())} for seg in raw]
    except Exception as exc:  # noqa: BLE001
        print(f"  youtube-transcript-api failed: {exc}")
        return None


def fetch_transcript_playwright(video_id: str) -> Optional[list]:
    """Last-resort: drive a headless browser and scrape the transcript panel."""
    try:
        from playwright.sync_api import sync_playwright  # noqa: WPS433
    except ImportError:
        return None
    url = f"https://www.youtube.com/watch?v={video_id}"
    segments: list = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(2500)
            for sel in ('button:has-text("Accept all")', 'button:has-text("I agree")',
                        'button[aria-label*="Accept"]'):
                try:
                    page.locator(sel).first.click(timeout=2000)
                    break
                except Exception:  # noqa: BLE001
                    pass
            try:
                page.locator("tp-yt-paper-button#expand, #expand").first.click(timeout=3000)
            except Exception:  # noqa: BLE001
                pass
            clicked = False
            for sel in ('button:has-text("Show transcript")',
                        '[aria-label="Show transcript"]',
                        'ytd-button-renderer:has-text("Show transcript")'):
                try:
                    page.locator(sel).first.click(timeout=3000)
                    clicked = True
                    break
                except Exception:  # noqa: BLE001
                    pass
            if not clicked:
                browser.close()
                return None
            page.wait_for_selector("ytd-transcript-segment-renderer", timeout=15000)
            items = page.locator("ytd-transcript-segment-renderer")
            for i in range(items.count()):
                el = items.nth(i)
                try:
                    ts = el.locator(".segment-timestamp").inner_text(timeout=2000).strip()
                    tx = el.locator(".segment-text").inner_text(timeout=2000).strip()
                except Exception:  # noqa: BLE001
                    continue
                segments.append({"ts_text": ts, "text": " ".join(tx.split())})
            browser.close()
    except Exception as exc:  # noqa: BLE001
        print(f"  playwright fallback failed: {exc}")
        return None
    return segments or None


# ------------------------------------------------------------------ writing
def _render_transcript_md(video_id, url, meta, segments, method) -> str:
    lines = [
        f"# Transcript: {meta.get('title') or video_id}",
        "",
        f"- Source: {url}",
        f"- Channel: {meta.get('channel_name') or ''}",
        f"- Video ID: {video_id}",
        f"- Fetched: {datetime.date.today().isoformat()}",
        f"- Method: {method}",
        "",
        "---",
        "",
    ]
    if not segments:
        lines.append("_(no transcript captured — paste the transcript here manually)_")
    for seg in segments:
        stamp = seg["ts_text"] if "ts_text" in seg else _ts(seg["start"])
        lines.append(f"[{stamp}] {seg['text']}")
    return "\n".join(lines) + "\n"


def fetch(url: str, channel_override: Optional[str] = None) -> dict:
    """Fetch metadata + transcript, write the references file, return a result dict."""
    video_id = extract_video_id(url)
    meta = fetch_metadata(url)
    channel_slug = channel_override or meta.get("channel_slug") or "unknown"

    segments = fetch_transcript_api(video_id)
    method = "youtube-transcript-api" if segments else None
    if not segments:
        segments = fetch_transcript_playwright(video_id)
        method = "playwright" if segments else "manual"
        if not segments:
            segments = []

    md = _render_transcript_md(video_id, url, meta, segments, method)
    ch_dir = config.YOUTUBE_REFS / channel_slug
    ch_dir.mkdir(parents=True, exist_ok=True)
    (ch_dir / f"{video_id}.md").write_text(md, encoding="utf-8")
    (ch_dir / "last.md").write_text(url + "\n", encoding="utf-8")

    rel_path = f"references/youtube/{channel_slug}/{video_id}.md"
    print(f"  transcript: {len(segments)} segment(s) via {method} -> {rel_path}")
    return {
        "video_id": video_id,
        "channel_slug": channel_slug,
        "meta": meta,
        "transcript_path": rel_path,
        "method": method,
        "has_timestamps": bool(segments),
        "language": meta.get("language", "en"),
    }

"""`kb new` — scaffold a content/videos/<id>/ folder + meta.json, and (by default)
fetch the transcript. This is the seam the summarizer sub-agents fill in next."""
from __future__ import annotations

import datetime
import json
from typing import Optional

from . import config, fetch as fetch_mod


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _stub(video_id: str, url: str) -> dict:
    now = _now_iso()
    return {
        "schema_version": 1,
        "video_id": video_id,
        "url": url,
        "title": "",
        "channel": "",
        "channel_name": "",
        "publish_date": None,
        "duration_seconds": None,
        "fetch_date": datetime.date.today().isoformat(),
        "topics": [],
        "concepts": [],
        "products": [],
        "people": [],
        "status": "queued",
        "analyses": {"summary": "summary.md", "detailed": "detailed.md", "deepdive": "deepdive.md"},
        "source": {"transcript_path": "", "transcript_method": "", "has_timestamps": False, "language": "en"},
        "created_at": now,
        "updated_at": now,
    }


def _merge_fetch(meta: dict, result: dict) -> None:
    m = result.get("meta", {})
    if m.get("title"):
        meta["title"] = m["title"]
    meta["channel"] = result.get("channel_slug") or meta.get("channel", "")
    if m.get("channel_name"):
        meta["channel_name"] = m["channel_name"]
    if m.get("publish_date"):
        meta["publish_date"] = m["publish_date"]
    if m.get("duration_seconds") is not None:
        meta["duration_seconds"] = m["duration_seconds"]
    meta["fetch_date"] = datetime.date.today().isoformat()
    meta["source"] = {
        "transcript_path": result["transcript_path"],
        "transcript_method": result["method"],
        "has_timestamps": result["has_timestamps"],
        "language": result.get("language", "en"),
    }
    if meta.get("status") in (None, "", "queued"):
        meta["status"] = "transcribed"
    meta["updated_at"] = _now_iso()


def _write_meta(video_id: str, meta: dict) -> None:
    vdir = config.VIDEOS_DIR / video_id
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_meta(video_id: str) -> Optional[dict]:
    path = config.VIDEOS_DIR / video_id / "meta.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def new(url: str, do_fetch: bool = True, channel: Optional[str] = None) -> str:
    video_id = fetch_mod.extract_video_id(url)
    meta = _load_meta(video_id) or _stub(video_id, url)
    if do_fetch:
        result = fetch_mod.fetch(url, channel_override=channel)
        _merge_fetch(meta, result)
    _write_meta(video_id, meta)
    print(f"  scaffolded content/videos/{video_id}/ (status: {meta['status']})")
    return video_id


def refetch(url: str, channel: Optional[str] = None) -> str:
    video_id = fetch_mod.extract_video_id(url)
    meta = _load_meta(video_id)
    if meta is None:
        raise SystemExit(f"no content/videos/{video_id}/meta.json — run `kb new {url}` first")
    result = fetch_mod.fetch(url, channel_override=channel)
    _merge_fetch(meta, result)
    _write_meta(video_id, meta)
    print(f"  refetched transcript for {video_id}")
    return video_id

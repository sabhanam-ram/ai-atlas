"""Render content/ -> docs/ as a static site (Markdown + Jinja2).

Internal links are RELATIVE (computed per page via ``rel``), so the output works
unchanged on local preview, user-pages, and project-pages — no base-url config.
"""
from __future__ import annotations

import posixpath
import shutil

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from . import config
from .index import Corpus, build_corpus, nav
from .models import Concept, Topic, VideoMeta
from .load import read_analysis
from .validate import validate

_md = markdown.Markdown(extensions=config.MARKDOWN_EXTENSIONS, output_format="html5")


def md_to_html(text: str | None) -> Markup:
    if not text:
        return Markup("")
    _md.reset()
    return Markup(_md.convert(text))


def first_paragraph(text: str | None, limit: int = 200) -> str:
    if not text:
        return ""
    for block in text.split("\n\n"):
        block = block.strip()
        if block and not block.startswith(("#", "---", "<!--")):
            block = " ".join(block.split())
            return block[:limit] + ("…" if len(block) > limit else "")
    return ""


def _rel_for(current_page: str):
    cur_dir = posixpath.dirname(current_page)
    def rel(target: str) -> str:
        if not target:
            return "#"
        return posixpath.relpath(target, cur_dir or ".")
    return rel


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _render_page(env: Environment, out_page: str, template: str, ctx: dict) -> None:
    tmpl = env.get_template(template)
    ctx = dict(ctx)
    ctx.setdefault("rel", _rel_for(out_page))
    ctx.setdefault("nav", nav())
    ctx.setdefault("site_title", config.SITE_TITLE)
    ctx.setdefault("site_tagline", config.SITE_TAGLINE)
    out_file = config.DOCS / out_page
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(tmpl.render(**ctx), encoding="utf-8")


# ---------------------------------------------------------------- view helpers
def _topic_chips(corpus: Corpus, video: VideoMeta) -> list[dict]:
    chips = []
    for slug in video.topics or []:
        t = corpus.topic_by_slug.get(slug)
        if t:
            chips.append({"display": t.display_name, "page": t.out_path, "kind": "topic"})
    return chips


def _concept_chips(corpus: Corpus, video: VideoMeta) -> list[dict]:
    chips = []
    for slug in video.concepts or []:
        co = corpus.concept_by_slug.get(slug)
        if co:
            chips.append({"display": co.display_name, "page": co.out_path, "kind": "concept"})
    return chips


def _video_card(corpus: Corpus, v: VideoMeta) -> dict:
    meta = " · ".join(p for p in [v.channel_name or v.channel, v.publish_date or "undated"] if p)
    return {
        "title": v.title or v.video_id,
        "page": v.out_path,
        "meta": meta,
        "desc": "",
        "chips": _topic_chips(corpus, v) + _concept_chips(corpus, v),
    }


# ---------------------------------------------------------------- page renders
def render_home(env: Environment, corpus: Corpus) -> None:
    cards = [_video_card(corpus, v) for v in corpus.videos_sorted()]
    _render_page(env, "index.html", "index.html", {
        "page_title": None,  # home uses the site title
        "intro": config.SITE_TAGLINE,
        "intro_sub": (f"{len(corpus.videos)} video(s) · {len(corpus.active_topics())} topic(s) · "
                      f"{len(corpus.concepts)} concept(s)"),
        "cards": cards,
        "empty_msg": "No videos processed yet. Run `python -m kb new <url>` to add one.",
    })


def render_video(env: Environment, corpus: Corpus, v: VideoMeta) -> None:
    analyses = []
    for key, _fn, label in config.ANALYSES:
        text = read_analysis(v, key)
        if text:
            analyses.append({"key": key, "label": label, "html": md_to_html(text)})
    src = v.source or {}
    _render_page(env, v.out_path, "video.html", {
        "page_title": v.title or v.video_id,
        "video": v,
        "topic_chips": _topic_chips(corpus, v),
        "concept_chips": _concept_chips(corpus, v),
        "analyses": analyses,
        "transcript_path": src.get("transcript_path", ""),
        "transcript_method": src.get("transcript_method", ""),
    })


def render_topic(env: Environment, corpus: Corpus, t: Topic) -> None:
    # mentions view
    mentions = []
    for m in t.mentions:
        vid = corpus.video_by_id.get(m.get("video_id"))
        mentions.append({
            "video_title": vid.title if vid else m.get("video_id"),
            "video_page": vid.out_path if vid else "",
            "anchor": m.get("anchor", ""),
            "channel": m.get("channel", ""),
            "published": m.get("published", ""),
            "analysis": m.get("analysis", ""),
            "section": m.get("section", ""),
            "claim": m.get("claim", ""),
        })
    timeline = []
    for r in corpus.topic_timeline(t):
        vid = r["video"]
        timeline.append({
            "date": r["date"], "channel": r["channel"], "products": r["products"],
            "claim": r["claim"],
            "video_page": vid.out_path if vid else "", "anchor": r["anchor"],
        })
    ref = None
    if t.concept_ref and t.concept_ref in corpus.concept_by_slug:
        co = corpus.concept_by_slug[t.concept_ref]
        ref = {"display": co.display_name, "page": co.out_path}
    related = [{"display": r.display_name, "page": r.out_path}
               for r in corpus.related_topics(t)]
    _render_page(env, t.out_path, "topic.html", {
        "page_title": t.display_name,
        "topic": t,
        "body_html": md_to_html(t.body_md),
        "video_count": len(corpus.topic_videos(t)),
        "mentions": mentions,
        "timeline": timeline,
        "concept_ref": ref,
        "related": related,
    })


def render_concept(env: Environment, corpus: Corpus, co: Concept) -> None:
    topics = [{"display": t.display_name, "page": t.out_path}
              for t in corpus.concept_topics.get(co.slug, [])]
    videos = [{"display": v.title or v.video_id, "page": v.out_path}
              for v in corpus.concept_videos.get(co.slug, [])]
    _render_page(env, co.out_path, "concept.html", {
        "page_title": co.display_name,
        "concept": co,
        "body_html": md_to_html(co.body_md),
        "topics": topics,
        "videos": videos,
    })


def render_topics_index(env: Environment, corpus: Corpus) -> None:
    cards = []
    for t in corpus.active_topics():
        cards.append({
            "title": t.display_name,
            "page": t.out_path,
            "meta": f"{t.mention_count} mention(s) · updated run {t.updated_run}",
            "desc": t.short_definition,
            "chips": [],
        })
    _render_page(env, "topics/index.html", "index.html", {
        "page_title": "Topics",
        "intro": "Topics",
        "intro_sub": "Recurring concepts correlated across every video.",
        "cards": cards,
        "empty_msg": "No topics yet.",
    })


def render_concepts_index(env: Environment, corpus: Corpus) -> None:
    cards = []
    for co in sorted(corpus.concepts, key=lambda x: x.display_name.lower()):
        cards.append({
            "title": co.display_name,
            "page": co.out_path,
            "meta": "concept reference",
            "desc": first_paragraph(co.body_md),
            "chips": [],
        })
    _render_page(env, "concepts/index.html", "index.html", {
        "page_title": "Concepts",
        "intro": "Concept reference library",
        "intro_sub": "Curated canonical definitions of core AI/agentic concepts.",
        "cards": cards,
        "empty_msg": "No concept docs yet.",
    })


# ---------------------------------------------------------------- build entry
def build(clean: bool = False) -> Corpus:
    corpus = build_corpus()
    errors, warnings = validate(corpus)
    for w in warnings:
        print(f"  warning: {w}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        raise SystemExit(f"build aborted: {len(errors)} validation error(s)")

    if clean and config.DOCS.exists():
        shutil.rmtree(config.DOCS)
    config.DOCS.mkdir(parents=True, exist_ok=True)

    env = _env()
    render_home(env, corpus)
    for v in corpus.videos:
        render_video(env, corpus, v)
    for t in corpus.topics:
        render_topic(env, corpus, t)
    for co in corpus.concepts:
        render_concept(env, corpus, co)
    render_topics_index(env, corpus)
    render_concepts_index(env, corpus)

    # assets
    (config.DOCS / ".nojekyll").write_text("", encoding="utf-8")
    css = config.STATIC_DIR / "style.css"
    if css.exists():
        shutil.copyfile(css, config.DOCS / "style.css")

    print(f"built {len(corpus.videos)} video(s), {len(corpus.active_topics())} topic(s), "
          f"{len(corpus.concepts)} concept(s) -> {config.DOCS}")
    return corpus

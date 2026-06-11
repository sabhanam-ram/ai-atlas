"""Read content/ into typed model objects. Pure reads — never mutates anything."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from . import config
from .models import Concept, Topic, VideoMeta


# ---------------------------------------------------------------- front matter
def parse_front_matter(text: str) -> tuple[dict, str]:
    """Parse a minimal ``key: value`` YAML-ish front-matter block.

    Returns (front_dict, body). Only simple scalars are supported (strings and
    ``null``); that is all our topic/concept files need, so we avoid a PyYAML
    dependency.
    """
    front: dict = {}
    if not text.startswith("---"):
        return front, text
    lines = text.splitlines()
    # find closing '---'
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return front, text
    for line in lines[1:end]:
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip().strip('"').strip("'")
        if val.lower() in ("null", "none", "~", ""):
            front[key.strip()] = None
        else:
            front[key.strip()] = val
    body = "\n".join(lines[end + 1:]).lstrip("\n")
    return front, body


def split_authored(body: str) -> str:
    """Return only the authored region of a topic body (everything before the
    generated marker)."""
    idx = body.find(config.GENERATED_MARKER_PREFIX)
    return body[:idx].rstrip() if idx != -1 else body.rstrip()


# ---------------------------------------------------------------- registry
def load_registry() -> dict:
    if not config.REGISTRY_PATH.exists():
        return {"schema_version": 1, "last_run": 0, "alias_index": {}, "topics": []}
    return json.loads(config.REGISTRY_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- videos
def load_videos() -> list[VideoMeta]:
    videos: list[VideoMeta] = []
    if not config.VIDEOS_DIR.exists():
        return videos
    for meta_path in sorted(config.VIDEOS_DIR.glob("*/meta.json")):
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        videos.append(VideoMeta.from_dict(data, directory=meta_path.parent))
    return videos


def read_analysis(video: VideoMeta, key: str) -> Optional[str]:
    """Read one analysis markdown file for a video, or None if absent."""
    if video.dir is None:
        return None
    filename = (video.analyses or {}).get(key)
    if not filename:
        # default convention
        filename = {"summary": "summary.md", "detailed": "detailed.md",
                    "deepdive": "deepdive.md"}.get(key)
    if not filename:
        return None
    path = video.dir / filename
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- topics
def load_topics(registry: Optional[dict] = None) -> list[Topic]:
    """Topics are authoritative in the registry; the .md supplies authored prose."""
    if registry is None:
        registry = load_registry()
    topics: list[Topic] = []
    for entry in registry.get("topics", []):
        topic = Topic.from_registry(entry)
        md_path = config.TOPICS_DIR / f"{topic.slug}.md"
        if md_path.exists():
            front, body = parse_front_matter(md_path.read_text(encoding="utf-8"))
            topic.front = front
            topic.body_md = split_authored(body)
            if not topic.display_name:
                topic.display_name = front.get("display_name", topic.slug)
        topics.append(topic)
    return topics


# ---------------------------------------------------------------- concepts
def load_concepts() -> list[Concept]:
    concepts: list[Concept] = []
    if not config.CONCEPTS_DIR.exists():
        return concepts
    for md_path in sorted(config.CONCEPTS_DIR.glob("*.md")):
        if md_path.name.startswith("_"):
            continue
        front, body = parse_front_matter(md_path.read_text(encoding="utf-8"))
        slug = front.get("slug") or md_path.stem
        concepts.append(Concept(
            slug=slug,
            display_name=front.get("display_name") or slug,
            body_md=body,
            front=front,
        ))
    return concepts

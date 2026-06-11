"""Typed views over the on-disk data. Loaded by kb.load, consumed by kb.render.

Templates access these with dot-notation (Jinja resolves attributes), so the
property helpers below double as the template API.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


def _fmt_duration(seconds: Optional[int]) -> str:
    if not seconds:
        return ""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


@dataclass
class VideoMeta:
    video_id: str
    url: str = ""
    title: str = ""
    channel: str = ""
    channel_name: str = ""
    publish_date: Optional[str] = None
    duration_seconds: Optional[int] = None
    fetch_date: Optional[str] = None
    topics: list = field(default_factory=list)
    concepts: list = field(default_factory=list)
    products: list = field(default_factory=list)
    people: list = field(default_factory=list)
    status: str = "queued"
    analyses: dict = field(default_factory=dict)
    source: dict = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # runtime-only (not from JSON)
    dir: Optional[Path] = None

    @classmethod
    def from_dict(cls, d: dict, directory: Optional[Path] = None) -> "VideoMeta":
        known = {f for f in cls.__dataclass_fields__ if f != "dir"}
        obj = cls(**{k: v for k, v in d.items() if k in known})
        obj.dir = directory
        return obj

    @property
    def out_path(self) -> str:
        return f"videos/{self.video_id}.html"

    @property
    def duration_display(self) -> str:
        return _fmt_duration(self.duration_seconds)


@dataclass
class Topic:
    """Combines the registry entry (correlation) with the authored .md body."""
    slug: str
    display_name: str = ""
    aliases: list = field(default_factory=list)
    short_definition: str = ""
    concept_ref: Optional[str] = None
    status: str = "active"
    created_run: int = 0
    updated_run: int = 0
    video_ids: list = field(default_factory=list)
    mentions: list = field(default_factory=list)
    merged_into: Optional[str] = None
    # from the .md file
    body_md: str = ""
    front: dict = field(default_factory=dict)

    @classmethod
    def from_registry(cls, d: dict) -> "Topic":
        known = {f for f in cls.__dataclass_fields__ if f not in ("body_md", "front")}
        return cls(**{k: v for k, v in d.items() if k in known})

    @property
    def out_path(self) -> str:
        return f"topics/{self.slug}.html"

    @property
    def mention_count(self) -> int:
        return len(self.mentions)


@dataclass
class Concept:
    slug: str
    display_name: str = ""
    body_md: str = ""
    front: dict = field(default_factory=dict)

    @property
    def out_path(self) -> str:
        return f"concepts/{self.slug}.html"

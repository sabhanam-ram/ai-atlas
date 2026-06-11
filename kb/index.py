"""Assemble the loaded content into a Corpus with cross-reference maps that the
renderer consumes (topic<->video, concept<->video, concept<->topic, related)."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import load
from .models import Concept, Topic, VideoMeta


def _pubkey(v: VideoMeta) -> str:
    # Sort newest first; videos with no date sort last.
    return v.publish_date or ""


@dataclass
class Corpus:
    registry: dict
    videos: list[VideoMeta]
    topics: list[Topic]
    concepts: list[Concept]
    video_by_id: dict = field(default_factory=dict)
    topic_by_slug: dict = field(default_factory=dict)
    concept_by_slug: dict = field(default_factory=dict)
    concept_videos: dict = field(default_factory=dict)   # concept slug -> [VideoMeta]
    concept_topics: dict = field(default_factory=dict)   # concept slug -> [Topic]

    def videos_sorted(self) -> list[VideoMeta]:
        return sorted(self.videos, key=_pubkey, reverse=True)

    def active_topics(self) -> list[Topic]:
        act = [t for t in self.topics if t.status == "active"]
        return sorted(act, key=lambda t: (-t.mention_count, t.display_name.lower()))

    def topic_videos(self, topic: Topic) -> list[VideoMeta]:
        vids = [self.video_by_id[vid] for vid in topic.video_ids if vid in self.video_by_id]
        return sorted(vids, key=_pubkey, reverse=True)

    def topic_timeline(self, topic: Topic) -> list[dict]:
        """One row per mention, oldest first, for the evolution timeline."""
        rows = []
        for m in topic.mentions:
            vid = self.video_by_id.get(m.get("video_id"))
            rows.append({
                "date": m.get("published") or "",
                "channel": m.get("channel", ""),
                "products": m.get("products", []) or [],
                "claim": m.get("claim", ""),
                "video": vid,
                "anchor": m.get("anchor", ""),
                "analysis": m.get("analysis", ""),
                "section": m.get("section", ""),
            })
        return sorted(rows, key=lambda r: r["date"])

    def related_topics(self, topic: Topic, limit: int = 6) -> list[Topic]:
        mine = set(topic.video_ids)
        scored = []
        for other in self.topics:
            if other.slug == topic.slug or other.status != "active":
                continue
            overlap = len(mine & set(other.video_ids))
            if overlap:
                scored.append((overlap, other))
        scored.sort(key=lambda x: (-x[0], x[1].display_name.lower()))
        return [t for _, t in scored[:limit]]


def build_corpus() -> Corpus:
    registry = load.load_registry()
    videos = load.load_videos()
    topics = load.load_topics(registry)
    concepts = load.load_concepts()

    c = Corpus(registry=registry, videos=videos, topics=topics, concepts=concepts)
    c.video_by_id = {v.video_id: v for v in videos}
    c.topic_by_slug = {t.slug: t for t in topics}
    c.concept_by_slug = {co.slug: co for co in concepts}

    # concept -> videos that list it
    for v in videos:
        for cslug in v.concepts or []:
            c.concept_videos.setdefault(cslug, []).append(v)
    # concept -> topics whose concept_ref points at it
    for t in topics:
        if t.concept_ref:
            c.concept_topics.setdefault(t.concept_ref, []).append(t)
    return c


def nav() -> list[dict]:
    """Top-nav items as doc-relative targets (rendered through rel())."""
    return [
        {"label": "Home", "page": "index.html"},
        {"label": "Topics", "page": "topics/index.html"},
        {"label": "Concepts", "page": "concepts/index.html"},
    ]

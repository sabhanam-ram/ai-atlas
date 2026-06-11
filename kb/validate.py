"""Consistency checks across meta.json, the topic registry, and the slug links.

Returns (errors, warnings). Errors must be zero before a build is trustworthy;
the CLI exits non-zero when any error is present.
"""
from __future__ import annotations

from . import config
from .index import Corpus, build_corpus


def validate(corpus: Corpus | None = None) -> tuple[list[str], list[str]]:
    c = corpus or build_corpus()
    errors: list[str] = []
    warnings: list[str] = []

    topic_slugs = set(c.topic_by_slug)
    concept_slugs = set(c.concept_by_slug)

    # 1. video.topics resolve to a registry topic
    for v in c.videos:
        for tslug in v.topics or []:
            if tslug not in topic_slugs:
                errors.append(f"video {v.video_id}: topic '{tslug}' not in registry")
        # 2. video.concepts resolve to a concept doc
        for cslug in v.concepts or []:
            if cslug not in concept_slugs:
                errors.append(f"video {v.video_id}: concept '{cslug}' has no content/concepts/{cslug}.md")

    # 3. topic.concept_ref resolves
    for t in c.topics:
        if t.concept_ref and t.concept_ref not in concept_slugs:
            errors.append(f"topic {t.slug}: concept_ref '{t.concept_ref}' has no concept doc")
        # topic should have an authored .md
        md_path = config.TOPICS_DIR / f"{t.slug}.md"
        if not md_path.exists():
            warnings.append(f"topic {t.slug}: no authored content/topics/{t.slug}.md")
        # 5. mentions point at known videos
        for m in t.mentions:
            vid = m.get("video_id")
            if vid not in c.video_by_id:
                errors.append(f"topic {t.slug}: mention references unknown video '{vid}'")

    # 4. alias_index values point at existing slugs
    for alias, slug in (c.registry.get("alias_index") or {}).items():
        if slug not in topic_slugs:
            errors.append(f"alias_index['{alias}'] -> '{slug}' which is not a topic")

    # 6. bidirectional video<->topic consistency
    reg_topic_videos: dict[str, set] = {t.slug: set(t.video_ids) for t in c.topics}
    for v in c.videos:
        declared = set(v.topics or [])
        from_registry = {slug for slug, vids in reg_topic_videos.items() if v.video_id in vids}
        missing_in_meta = from_registry - declared
        missing_in_registry = declared - from_registry
        if missing_in_meta:
            warnings.append(
                f"video {v.video_id}: registry links topics {sorted(missing_in_meta)} "
                f"but meta.topics omits them")
        if missing_in_registry:
            errors.append(
                f"video {v.video_id}: meta.topics lists {sorted(missing_in_registry)} "
                f"but registry has no mention linking them")

    return errors, warnings

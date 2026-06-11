"""Shared paths and constants. One place defines where everything lives."""
from __future__ import annotations

from pathlib import Path

# Repo root = parent of the kb/ package directory.
ROOT = Path(__file__).resolve().parent.parent

# Authored / generated content (what agents write).
CONTENT = ROOT / "content"
VIDEOS_DIR = CONTENT / "videos"
TOPICS_DIR = CONTENT / "topics"
CONCEPTS_DIR = CONTENT / "concepts"
REGISTRY_PATH = TOPICS_DIR / "_registry.json"
AGENT_LOG_PATH = TOPICS_DIR / "_agent_log.md"

# Raw provenance.
REFERENCES = ROOT / "references"
YOUTUBE_REFS = REFERENCES / "youtube"

# Renderer.
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"

# Generated static site (GitHub Pages serves this directory).
DOCS = ROOT / "docs"

# Markdown extensions used everywhere we render Markdown -> HTML.
MARKDOWN_EXTENSIONS = ["extra", "fenced_code", "tables", "toc", "sane_lists"]

# Everything ABOVE this marker in a topic .md is authored; below is regenerated.
# Match on this prefix (dash style after it may vary).
GENERATED_MARKER_PREFIX = "<!-- GENERATED"

SITE_TITLE = "learning-ai"
SITE_TAGLINE = "A knowledge base built from AI/agentic YouTube research"

# The three analysis artifacts, in display order: (key, filename, label).
ANALYSES = [
    ("summary", "summary.md", "Summary"),
    ("detailed", "detailed.md", "Detailed analysis"),
    ("deepdive", "deepdive.md", "Deep-dive analysis"),
]

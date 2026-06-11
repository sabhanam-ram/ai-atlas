"""Deterministic slug + phrase-normalization helpers, used everywhere so that
cross-links (channel / topic / concept) stay stable."""
from __future__ import annotations

import re
import unicodedata


def _ascii_fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text))
    return text.encode("ascii", "ignore").decode("ascii")


def slugify(text: str) -> str:
    """lowercase -> ASCII-fold -> non-alphanumerics to single hyphens -> trim."""
    text = _ascii_fold(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def normalize_phrase(text: str) -> str:
    """Normalize a concept phrase for alias matching:
    lowercase, ASCII-fold, collapse whitespace/hyphens to single spaces, trim."""
    text = _ascii_fold(text).lower()
    text = re.sub(r"[\s\-]+", " ", text)
    return text.strip()

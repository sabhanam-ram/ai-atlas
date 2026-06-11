# GitHub Copilot — Repository Instructions

The authoritative instructions for this repository are in **`AGENTS.md`** at the repo root.
**Before doing any work here, open `AGENTS.md` and follow it exactly.** This file is only a
pointer and deliberately does not restate the contract.

## Context

`learning-ai` is an agent-driven knowledge base built from AI/agentic YouTube videos. The
pipeline fetches a transcript; an agent then writes three analyses (summary / detailed /
deep-dive), correlates recurring topics in `content/topics/_registry.json`, and a Python
build (`python -m kb build`) renders a static site into `docs/`.

## When asked to add or process a video

Treat a short request like **"add this video: <url>"** as the full ingestion pipeline in
`AGENTS.md` (§1 + §5), using the project venv (`.\.venv\Scripts\python.exe`):

1. `python -m kb new <url>` — scaffold the video folder + `meta.json` and fetch the transcript.
2. Read `references/youtube/<channel>/<id>.md`.
3. Write `summary.md` / `detailed.md` / `deepdive.md` in `content/videos/<id>/`
   (no leading `#` heading — the template supplies it).
4. Correlate topics in `content/topics/_registry.json` per `AGENTS.md` §5; author/extend the
   topic `.md` files; set `topics`/`concepts` in `meta.json`; log the run.
5. `python -m kb validate` (must pass) → `python -m kb build --clean`.

## Key rules (full detail in `AGENTS.md`)

- Write **only** under `references/` and `content/`. Never hand-edit `docs/` (generated) or
  the `kb/` renderer to make content appear.
- `content/topics/_registry.json` is the source of truth for correlation.
- Cross-links are by slug, resolved at build time — reference a slug with no source file and
  `kb build` / `kb validate` fails. Create the file first.

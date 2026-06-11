# CLAUDE.md

The full, authoritative instructions for working in this repository live in
**[`AGENTS.md`](AGENTS.md)** — read it first and follow it exactly. This file is only a
router; it intentionally does **not** duplicate the contract.

@AGENTS.md

## What this repo is (one line)

**AI Atlas** — an agent-driven knowledge base built from AI/agentic YouTube videos: fetch a
transcript, write three analyses, correlate recurring topics, and render a static site into
`docs/`.

## When you are asked to add / process a video

A short instruction such as **"add this video: <url>"** means: run the full ingestion
pipeline documented in `AGENTS.md` (§1 pipeline + §5 append protocol). In brief, using the
venv interpreter (`.\.venv\Scripts\python.exe`):

1. `python -m kb new <url>` — scaffolds `content/videos/<id>/` + `meta.json` and fetches the
   transcript to `references/youtube/<channel>/<id>.md`.
2. Read that transcript, then write `summary.md`, `detailed.md`, `deepdive.md` in the video
   folder (no leading `#` heading — the page template supplies it).
3. Correlate per `AGENTS.md` §5: update `content/topics/_registry.json`, author/extend the
   topic `.md` files, set `topics`/`concepts` in `meta.json`, and log the run.
4. `python -m kb validate` (must pass) → `python -m kb build --clean`.

The golden rules (write only under `references/` + `content/`; never hand-edit `docs/`;
cross-link by slug or the build fails) and every detail are in `AGENTS.md`.

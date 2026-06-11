# AI Atlas

An **agent-driven knowledge base** built from research on AI / agentic **YouTube
channels**. For each video, an agent fetches the transcript and writes a **summary**, a
**detailed analysis**, and a **deep-dive analysis**. Recurring concepts (Agent Memory,
RAG, MCP, tool use, …) are **correlated across videos and over time** on topic pages with
an evolution timeline. Everything renders to a browsable static HTML site.

> **If you are an AI agent**, do not start here — read **[`AGENTS.md`](AGENTS.md)** first.
> It is the processing contract: the pipeline, the file layout, the `meta.json` schema, and
> the append protocol for adding a new video without re-reading the whole corpus.

## What's where

| Path | Purpose |
|------|---------|
| `AGENTS.md` | The authoritative AI-agent contract — read first |
| `CLAUDE.md` · `.github/copilot-instructions.md` | Per-tool entry points — thin routers to `AGENTS.md` |
| `references/youtube/<channel>/<id>.md` | Raw fetched transcripts (provenance) |
| `content/videos/<id>/` | Per-video `meta.json` + `summary.md` / `detailed.md` / `deepdive.md` |
| `content/topics/_registry.json` | Source of truth for cross-video topic correlation |
| `content/topics/<slug>.md` | Authored topic synthesis (timeline/backlinks are generated) |
| `content/concepts/<slug>.md` | Curated canonical concept definitions ("AI-readiness" docs) |
| `kb/` | Python build pipeline (fetch + render) |
| `templates/`, `static/` | Jinja2 templates + CSS |
| `docs/` | **Generated** static site (GitHub Pages serves this) |

## Quickstart (Windows / PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium   # fallback only

# Add a video (scaffolds content/videos/<id>/ and fetches the transcript)
.\.venv\Scripts\python.exe -m kb new https://www.youtube.com/watch?v=VIDEO_ID

# ...an agent then writes the three analyses and registers topics (see AGENTS.md)...

.\.venv\Scripts\python.exe -m kb validate      # check data + links
.\.venv\Scripts\python.exe -m kb build --clean # render content/ -> docs/
.\.venv\Scripts\python.exe -m http.server -d docs 8000   # preview at http://localhost:8000/
```

## Publishing

The build emits GitHub-Pages-compatible output into `docs/` (includes `.nojekyll`). Enable
Pages via **Settings → Pages → Deploy from branch → `main` / `/docs`**. Internal links are
**relative**, so the site works unchanged on local preview, user-pages, and project-pages
(`<user>.github.io/ai-atlas/`) with no base-URL configuration.

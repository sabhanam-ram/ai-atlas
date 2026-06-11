# AGENTS.md — Processing Contract

> **FOR AI AGENTS: read this file first.** It defines how to add a YouTube video to this
> knowledge base and how to keep the cross-video topic correlation consistent. Follow it
> exactly. Humans: see `README.md`.

This repo turns AI/agentic **YouTube videos** into a browsable, AI-navigable knowledge
base. For each video an agent fetches the transcript, writes three analyses, and records
how the video's concepts relate to every other video. A Python build renders it all to a
static site in `docs/`.

> `CLAUDE.md` (Claude Code) and `.github/copilot-instructions.md` (GitHub Copilot) are thin
> routers that point here — **this file is the single source of truth.**

---

## Quickstart — adding one video (TL;DR)

If you were invoked with a short prompt like "add/process this video: <url>", do this, using
the venv interpreter (`.\.venv\Scripts\python.exe`):

1. `python -m kb new <url>` — scaffolds `content/videos/<id>/` + `meta.json` and fetches the
   transcript to `references/youtube/<channel>/<id>.md`.
2. Read that transcript. Write `summary.md`, `detailed.md`, `deepdive.md` in the video folder
   (no leading `#` heading — see §3).
3. Correlate: follow the **append protocol (§5)** to update `content/topics/_registry.json`,
   author/extend the topic `.md` files, set `topics`/`concepts` in `meta.json`, and log the
   run in `content/topics/_agent_log.md`.
4. `python -m kb validate` (must pass) → `python -m kb build --clean`.

The rest of this file is the detail behind each step — read it before your first ingestion.

---

## 0. Golden rules

1. **You only write under `references/` and `content/`.** Never hand-edit `docs/` (it is
   generated) or the `kb/` renderer to make content appear.
2. **`content/topics/_registry.json` is the source of truth for correlation.** All
   cross-video relationships live there. Read it before touching topics.
3. **Cross-links are by slug, resolved at build time.** If you reference a topic/concept
   slug that has no source file, `kb build` / `kb validate` **fails**. Create the file
   first.
4. **The build never mutates content.** It only reads `content/` + `templates/` +
   `static/` and writes `docs/`. Re-running it produces the same output.

---

## 1. The pipeline (per video)

```
kb new <url>        ->  scaffold content/videos/<id>/ + meta.json (status: queued)
kb fetch <url>      ->  references/youtube/<channel>/<id>.md   (status: transcribed)
   (you) author     ->  summary.md, detailed.md, deepdive.md   (status: analyzed)
   (you) correlate  ->  update _registry.json + topic .md      (append protocol, §5)
kb build            ->  docs/...html
kb validate         ->  asserts data + links are consistent
```

Run the CLI through the venv interpreter:
```
.\.venv\Scripts\python.exe -m kb <new|fetch|build|validate> [args]
```

`kb new` calls `kb fetch` for you. If automated fetch fails (no captions / age gate), set
`source.transcript_method = "manual"` and paste the transcript into the `references/…md`
file yourself using the format in §4.

---

## 2. Directory layout

```
references/youtube/<channel-slug>/<video_id>.md   # raw transcript (provenance)
references/youtube/<channel-slug>/last.md         # pointer to last-fetched URL
content/videos/<video_id>/meta.json               # machine record (§3)
content/videos/<video_id>/summary.md              # analysis 1
content/videos/<video_id>/detailed.md             # analysis 2
content/videos/<video_id>/deepdive.md             # analysis 3
content/topics/_registry.json                     # correlation source of truth (§5)
content/topics/_agent_log.md                      # dated run log
content/topics/<topic-slug>.md                    # authored topic synthesis (§6)
content/concepts/<concept-slug>.md                # curated canonical definition (§7)
```

`<video_id>` is the YouTube 11-char id. `<channel-slug>` and topic/concept slugs all use
the same slug rule: lowercase, ASCII, spaces/punctuation → single hyphens (see
`kb/slug.py`, function `slugify`).

---

## 3. `meta.json` schema + status lifecycle

```jsonc
{
  "schema_version": 1,
  "video_id": "abc123XYZ_0",
  "url": "https://www.youtube.com/watch?v=abc123XYZ_0",
  "title": "Full video title",
  "channel": "channel-slug",
  "channel_name": "Channel Display Name",
  "publish_date": "2026-05-01",       // ISO date or null
  "duration_seconds": 1730,            // int or null
  "fetch_date": "2026-06-11",
  "topics":   ["agent-memory", "rag"], // resolved topic slugs (must exist in _registry.json)
  "concepts": ["rag", "tool-use"],     // concept slugs (content/concepts/<slug>.md must exist)
  "products": ["LangGraph", "Claude"], // free-text product mentions
  "people":   ["Jane Doe"],            // free-text people mentions
  "status":   "rendered",              // see lifecycle below
  "analyses": { "summary": "summary.md", "detailed": "detailed.md", "deepdive": "deepdive.md" },
  "source": {
    "transcript_path": "references/youtube/channel-slug/abc123XYZ_0.md",
    "transcript_method": "youtube-transcript-api", // yt-dlp | youtube-transcript-api | playwright | manual
    "has_timestamps": true,
    "language": "en"
  },
  "created_at": "2026-06-11T00:00:00Z",
  "updated_at": "2026-06-11T00:00:00Z"
}
```

**`status` lifecycle** (advance as you complete each stage):
`queued` → `transcribed` → `summarized` → `analyzed` → `rendered`

- `topics` here is the resolved slug list (the join key for the build). The rich
  per-mention detail (claim, section, anchor, products) lives in `_registry.json`, **not**
  here. `kb validate` checks the two agree.
- Every slug in `concepts[]` MUST have a `content/concepts/<slug>.md`. If the canonical
  doc does not exist yet, either author it (§7) or drop the slug — do not leave a dangling
  reference.

**Writing the three analyses:** do NOT start `summary.md` / `detailed.md` / `deepdive.md`
with a top-level `# Heading` — the page template already renders the section label
("Summary" / "Detailed analysis" / "Deep-dive analysis"). Begin with body prose; use `##`
for any sub-sections. The mention `anchor` values `summary` / `detailed` / `deepdive` are
the ids of these three sections on the rendered video page.

---

## 4. Transcript file format (`references/youtube/<channel>/<id>.md`)

```
# Transcript: <video title>

- Source: <full youtube url>
- Channel: <channel display name>
- Video ID: <id>
- Fetched: <YYYY-MM-DD>
- Method: <yt-dlp | youtube-transcript-api | playwright | manual>

---

[00:00] First line / paragraph of transcript text.
[00:12] Next segment...
```

`last.md` in the same channel folder holds just the most-recently-fetched URL (one line).
Timestamps `[mm:ss]` are preferred (they let mention `section`/`anchor` deep-link); if the
source has none, set `source.has_timestamps = false` and write plain paragraphs.

---

## 5. Append protocol — adding a NEW video to the correlation layer

This is the critical procedure. It lets you relate a new video to all prior ones by
reading **only** `_registry.json`, `_agent_log.md`, and this video's `meta.json` — never
the other videos' files.

1. **Read** `content/topics/_registry.json` fully. The new run number is `last_run + 1`.
2. From your analyses, list the **concepts the video actually discusses**. For each, note:
   which analysis (`summary`/`detailed`/`deep-dive`), a `section` locator (a `[mm:ss]` or
   heading), a one-sentence `claim` (what *this* video says about it), and any `products`.
3. For each concept phrase, **normalize** it (lowercase, trim, collapse whitespace/hyphens
   to single spaces) and resolve a topic:
   - `alias_index[normalized]` exists → **REUSE** that `slug`.
   - else a confident token-overlap match against an existing `display_name`/alias →
     **REUSE** that slug **and** add `normalized` to that topic's `aliases` + to
     `alias_index`.
   - else → **CREATE** a new topic (next step).
4. **Reuse path:** append a mention object to the topic's `mentions[]` (dedupe: skip if a
   mention with the same `video_id`+`analysis` already exists). Add `video_id` to
   `video_ids`. Set the topic's `updated_run`. If the new claim adds something materially
   new, revise ONLY the authored prose in `content/topics/<slug>.md` (above the sentinel,
   §6) and bump its `synthesis_updated_run`. If it only restates known points, leave the
   `.md` alone — the generated timeline/mentions still update automatically.
5. **Create path:** make a slug; ensure it is unique. Append a topic object with
   `display_name`, `aliases:[normalized]`, a one-line `short_definition`, `concept_ref`
   (an existing concept slug, else `null`), `status:"active"`,
   `created_run`/`updated_run` = run, the first mention, `video_ids:[video_id]`. Add the
   alias→slug entry to `alias_index`. Create `content/topics/<slug>.md` (§6) seeded from
   this video's claim. If `concept_ref` is null, note a curator TODO in the log.
6. **Write back the video's `meta.json`:** set `topics` to the resolved slug list; set
   `concepts` to the concept-doc slugs you linked; advance `status`; update `updated_at`.
7. **Bump the registry:** `last_updated` = today, `last_run` = run. Write the whole file.
8. **Log one line** in `content/topics/_agent_log.md` (format is in that file's header).

A mention object:
```jsonc
{ "video_id":"<id>", "channel":"<channel-slug>", "published":"YYYY-MM-DD",
  "analysis":"summary|detailed|deep-dive", "section":"12:40", "anchor":"<heading-anchor>",
  "claim":"one sentence", "products":["..."], "added_run": <n> }
```
`channel`/`published`/`products`/`claim` are denormalized into each mention on purpose, so
later runs (and the build) never have to open other videos' files.

---

## 6. Topic page source (`content/topics/<slug>.md`)

Authored prose only. The build appends generated sections (mentions list, evolution
timeline, related topics, reference box) below the sentinel — **never** write those by hand.

```markdown
---
slug: agent-memory
display_name: Agent Memory
concept_ref: agent-memory      # or null
synthesis_updated_run: 1
---

## Canonical synthesis

2–5 paragraphs reconciling how the different videos explain this concept; note where they
agree/disagree.

## Key distinctions

- ...

<!-- GENERATED BELOW — DO NOT EDIT -->
```

Everything above `<!-- GENERATED BELOW — DO NOT EDIT -->` is yours. The build ignores
anything you put below it and regenerates that region.

---

## 7. Concept-reference library (`content/concepts/<slug>.md`)

Curated, stable, canonical definitions (the "AI-readiness" docs) — e.g. `rag.md`,
`agent-memory.md`, `mcp.md`, `tool-use.md`. These change rarely. A topic page links to its
`concept_ref`; the concept page back-links to the topics/videos that reference it
(generated). Front matter:

```markdown
---
slug: rag
display_name: Retrieval-Augmented Generation (RAG)
---

Canonical explanation...
```

---

## 8. Slug rules

- One function: `kb/slug.py::slugify`. lowercase → ASCII-fold → non-alphanumerics to single
  hyphens → trim hyphens. Use it for channel, topic, and concept slugs so links are stable.
- A topic slug, once created, **never changes** (it is the join key). To retire a topic,
  set `status:"merged"` + `merged_into:"<slug>"` rather than deleting it.

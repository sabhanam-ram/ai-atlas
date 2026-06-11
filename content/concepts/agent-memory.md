---
slug: agent-memory
display_name: Agent Memory
---

**Agent memory** is how an AI agent persists and retrieves information across the
boundaries of a single model call — within a multi-turn task, and across separate
sessions. Because a language model is stateless and bounded by its context window, any
durable "memory" must live outside the weights and be selectively loaded back into the
prompt when relevant.

## The layers of memory

- **Working / short-term memory** — the contents of the current context window: the
  system prompt, the running conversation, scratchpad reasoning, and recently used tool
  results. It is fast but finite and disappears when the context is cleared.
- **Long-term memory** — an external store (a database, file, or vector index) that
  outlives any single context. Writing to it and reading from it are explicit actions.

A common further split of long-term memory:

- **Episodic** — a log of what happened: past events, prior conversations, decisions taken.
- **Semantic** — distilled facts and knowledge: user preferences, learned procedures,
  durable truths extracted from episodes.
- **Procedural** — learned skills/instructions the agent reuses (often captured as updated
  prompts or playbooks).

## How it works in practice

Long-term memory is usually implemented as a retrieval store: the agent writes salient
information (a summary, a fact, an outcome), embeds it, and later retrieves the most
relevant entries to reload into the working context — making memory a specialized
application of [retrieval-augmented generation](rag.html). Reading and writing memory are
typically exposed to the model as [tools](tool-use.html), so the agent decides what is
worth remembering and when to recall it.

## Key tensions

- **What to store** — storing everything pollutes retrieval; storing too little loses
  signal. Summarization and salience judgments matter.
- **When to recall** — recall must be triggered by relevance, not dumped wholesale, or it
  crowds out the working context.
- **Consistency over time** — when facts change (a preference updates, a product is
  upgraded), memory must be revised, not merely appended, to avoid contradictions.

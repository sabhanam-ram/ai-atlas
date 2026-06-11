---
slug: context-engineering
display_name: Context Engineering
concept_ref: agent-memory
synthesis_updated_run: 1
---

## Canonical synthesis

**Context engineering** is the deliberate management of what occupies a model's finite
context window — the working (short-term) layer of [agent memory](../concepts/agent-memory.html).
In the building-agents discussion it shows up as a primary *motivation* for
[multi-agent systems](multi-agent-systems.html): sub-agents are used not only for parallelism
but to **protect the main context**.

The canonical example: in Claude Code, a subtask that would consume tens of thousands of
tokens — like locating a specific class implementation — but whose answer "boils down to
something very small" is offloaded to a sub-agent. The sub-agent does the token-heavy work in
its own window and returns only the small final result, so the orchestrator's context stays
focused. Splitting a large tool set (100–200 tools) into ~20-tool buckets per sub-agent
applies the same principle to the *tool namespace*: keep each agent's decision space small.

## Key distinctions

- **Working memory, not long-term memory** — this is about the live context window, distinct
  from persistent stores; see [agent memory](../concepts/agent-memory.html) for the full
  memory hierarchy.
- **Offloading vs. summarizing** — sub-agent offloading isolates work in a separate window;
  summarization compresses within the same window. Both shrink what the main loop must hold.

<!-- GENERATED BELOW — DO NOT EDIT -->

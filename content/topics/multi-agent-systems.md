---
slug: multi-agent-systems
display_name: Multi-Agent Systems
concept_ref: null
synthesis_updated_run: 1
---

## Canonical synthesis

A **multi-agent system** runs more than one model instance concurrently to solve a single
problem. The dominant shape is **orchestrator/worker**: a parent agent decomposes a task and
delegates pieces to sub-agents that run in parallel, then integrates their results. Anthropic
ships this in production — *Deep Research* spawns parallel search sub-agents so the user gets
an answer sooner, and *Claude Code* uses sub-agents to absorb token-heavy subtasks.

The key implementation insight is that multi-agent is **not a new paradigm** — it is built on
ordinary [tool use](../concepts/tool-use.html): to the parent model, a sub-agent "looks like
a tool" that takes a prompt and returns a result. There is no separate coordination protocol;
the tool handler just happens to launch another model loop.

Two motivations recur: **parallelism** (MapReduce-style work, diverse parallel attempts as a
form of *test-time compute*) and **context isolation** (keeping each agent's window and tool
set small — see [Context Engineering](context-engineering.html)).

## Key distinctions

- **vs. workflows of agents** — in a workflow of agents, one agent finishes and hands off to
  the next (sequential). In a multi-agent system, agents work *at the same time*. See
  [Agents vs. Workflows](agents-vs-workflows.html).
- **Manager quality is the bottleneck** — early on, a model delegates like a first-time
  manager: under-specified instructions, assumed-but-absent context. Better delegation
  (clear instructions, full context to sub-agents) is an active training target.
- **Overbuilding is the main failure mode** — too many agents create communication overhead
  and "dead weight," mirroring large human organizations; start simple.

<!-- GENERATED BELOW — DO NOT EDIT -->

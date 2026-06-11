---
slug: agents-vs-workflows
display_name: Agents vs. Workflows
concept_ref: null
synthesis_updated_run: 1
---

## Canonical synthesis

This is the architectural spectrum for orchestrating model calls:

- **Workflows** — predefined chains of prompts. Best when you need low latency and a single
  best-effort answer in one shot. Brittle to failure: if one step silently fails (e.g. a SQL
  query returns nothing), downstream steps proceed on bad input.
- **Agents** — a model run in a *loop*: it acts, observes the result, and iterates,
  self-correcting until done. As models got better at responding to feedback, agent loops
  came to "dramatically outperform workflows for most things where you care most about
  absolute quality."
- **Workflows of agents** — the hybrid: keep an overall workflow, but make *each step* a
  closed agent loop that iterates until it has a correct result before advancing. This fixes
  the brittleness of plain workflows while retaining structure.

The standing advice is **start simple** — single-shot or a single agent loop — and add layers
only as needed, because complexity hurts observability.

## Key distinctions

- **vs. multi-agent** — workflows of agents are *sequential* (one step hands off to the next);
  [multi-agent systems](multi-agent-systems.html) run agents *concurrently*.
- **Latency vs. quality** — workflows favor latency/predictability; agent loops favor quality
  and robustness. The choice is a trade-off, not a verdict.

<!-- GENERATED BELOW — DO NOT EDIT -->

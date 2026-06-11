---
slug: tool-use
display_name: Tool Use
concept_ref: tool-use
synthesis_updated_run: 1
---

## Canonical synthesis

**Tool use** (function calling) is the primitive that lets a model act: the application
declares tools with schemas, the model emits a structured call, the application executes it,
and the result re-enters the context. In the agents discussion it emerges as the *substrate*
beneath nearly everything else — [multi-agent](multi-agent-systems.html) sub-agents are tool
calls whose handlers launch more models; retrieval is a tool the agent calls; and
[MCP](mcp.html) is a standard way to expose tools.

The most actionable design principle surfaced so far: **design tools (and MCP servers) 1:1
with your UI, not your API**, because "the model is a user of these things." A tool should
return a complete, rendered result in one call and minimize round-trips, rather than mirror
fine-grained API endpoints that force the model to chain several calls to assemble one view.

## Key distinctions

- **Tool calling as a communication protocol** — the same mechanism that calls a search API
  also invokes a sub-agent; the uniformity is what makes agent architectures composable.
- **Tool-set size matters** — large tool sets (100–200 tools) degrade selection; splitting
  them across sub-agents (~20 each) keeps each decision space tractable.
- **Quality of description = quality of use** — the model can only use a tool as well as its
  description and schema allow; "think from the agent's point of view" and read exactly what
  the model sees.

<!-- GENERATED BELOW — DO NOT EDIT -->

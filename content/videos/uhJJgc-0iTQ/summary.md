A conversation between **Alex** (who leads Claude Relations at Anthropic) and **Erik**
(multi-agent research at Anthropic) on how to build more effective AI agents.

- **Why Claude is good at agent tasks:** during training it is given open-ended, multi-step
  problems and practices "being an agent" — taking many steps and using tools before giving
  a final answer — reinforced heavily on coding and search. (00:33)
- **Coding is the foundational skill:** "train on the hardest thing first." A strong coding
  agent generalizes to non-coding work — web search, planning, and producing artifacts by
  *writing code* (e.g. a script that emits an Excel file or repetitive SVG). (01:26)
- **Claude Code SDK:** a ready-made, polished agent loop so developers don't rebuild the
  loop, tool execution, file handling, and MCP wiring themselves; it's a general-purpose
  agent that you customize by swapping in your own tools via MCP. (03:23)
- **Skills:** an extension of `CLAUDE.md` from instructions-only to bundling reusable
  *resources* (templates, scripts, assets) — the "Matrix kung-fu download" analogy. (05:29)
- **Workflows → agents → "workflows of agents":** agent loops now beat rigid workflows on
  quality because Claude self-corrects; workflows still win for low-latency single-shot; the
  emerging pattern wraps each workflow step in its own closed agent loop. (06:42)
- **Multi-agent:** an orchestrator delegates to sub-agents running in parallel (as in Deep
  Research and Claude Code). Sub-agents are invoked through the tool-calling framework and
  are used to parallelize work and to **protect the main context**. (09:44)
- **Best practices:** start simple and add complexity only as needed; "think from the
  agent's point of view" — read exactly what the model sees; design tools/MCPs **1:1 with
  your UI, not your API**. (15:12)
- **The future:** agents spreading outward from verifiable domains (software engineering),
  self-verifying via computer use, and acting directly inside apps. (16:59)

---
slug: mcp
display_name: Model Context Protocol (MCP)
concept_ref: mcp
synthesis_updated_run: 1
---

## Canonical synthesis

The **Model Context Protocol (MCP)** is the standard surface for connecting an agent to
external tools and data. In the building-agents context it appears as the recommended way to
**extend a ready-made agent loop**: the Claude Code SDK already implements the loop, tool
execution, and file handling, and developers "just add their tools for their own custom
business logic … via MCP."

The design guidance attached to MCP is the same as for [tool use](tool-use.html) generally:
an MCP server should map **1:1 to your UI, not your API**. Since the model consumes the
server's output the way a person consumes a screen, a server should return a complete,
rendered result in a single call rather than expose many low-level endpoints that force the
model into multiple round-trips (the Slack example: one "read the conversation" tool instead
of separate conversation / user-ID / channel-ID lookups).

## Key distinctions

- **MCP vs. raw tool definitions** — MCP standardizes the *integration surface* so a tool
  built once is reusable across applications; the underlying call is still ordinary tool use.
- **Customization seam** — MCP is where bespoke business logic plugs into an otherwise generic
  agent loop (Claude Code SDK).

<!-- GENERATED BELOW — DO NOT EDIT -->

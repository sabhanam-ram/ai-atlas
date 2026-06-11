---
slug: mcp
display_name: Model Context Protocol (MCP)
---

The **Model Context Protocol (MCP)** is an open standard for connecting AI applications
to external tools, data sources, and prompts through a uniform interface. Introduced by
Anthropic in late 2024, it plays a role often described as "a USB-C port for AI" — one
protocol that lets any compliant host connect to any compliant server, instead of every
application hand-building a bespoke integration for every data source.

## The problem it solves

Before a standard, each AI app integrated each tool/datasource with its own custom glue
code — an N×M explosion of one-off connectors. MCP turns this into N+M: a tool author
writes one **MCP server**; an application author writes one **MCP client**; any client can
then talk to any server.

## Architecture

- **Host** — the AI application the user interacts with (e.g. an IDE assistant or chat app).
- **Client** — lives inside the host and maintains a 1:1 connection to a server.
- **Server** — a lightweight program exposing capabilities over the protocol.

Servers expose three main primitives:

- **Tools** — callable functions the model can invoke (see [tool use](tool-use.html)).
- **Resources** — readable data/content the host can pull in as context.
- **Prompts** — reusable, parameterized prompt templates.

Communication uses JSON-RPC, over local transports (stdio) or remote ones (HTTP, typically
with Server-Sent Events for streaming).

## Why it matters

MCP standardizes the *integration surface* of agentic systems. It makes [tool use](tool-use.html)
portable across applications, lets [retrieval](rag.html) sources be shared as servers, and
gives long-term [memory](agent-memory.html) stores a common way to be plugged into any
host — so capabilities built once are reusable everywhere the protocol is supported.

---
slug: tool-use
display_name: Tool Use (Function Calling)
---

**Tool use** (also called *function calling*) is the mechanism by which a language model
takes actions in the world beyond producing text. The model is told, in a structured way,
which tools exist and what arguments they accept; when it decides a tool is needed, it
emits a structured call; the application executes that call and returns the result to the
model, which then continues reasoning with the new information.

## The loop

1. **Declare** — the application gives the model a set of tool definitions (name,
   description, and a JSON schema for the inputs).
2. **Decide & call** — given a task, the model either answers directly or emits a tool
   call with arguments matching the schema.
3. **Execute** — the application (not the model) runs the tool and captures the result.
4. **Observe & continue** — the result is fed back into the context; the model may call
   more tools, then produce a final answer.

This observe-act loop, repeated, is the engine underneath most **agents**: an agent is
largely a model in a loop with tools.

## Why it is foundational

- It connects a stateless text predictor to live systems — search, code execution,
  databases, APIs, and other services.
- It is the substrate for higher-level patterns: [retrieval](rag.html) is a tool the model
  calls to fetch context; [agent memory](agent-memory.html) is implemented as
  read/write memory tools; and [MCP](mcp.html) is a standard way to expose tools to many
  applications at once.

## What makes it reliable (or not)

- **Clear tool descriptions and schemas** — the model can only use a tool as well as it is
  described; ambiguous descriptions cause wrong or missing calls.
- **Few, well-chosen tools** beat many overlapping ones — too many tools dilute the model's
  selection accuracy.
- **Robust execution & error handling** — returning a useful error lets the model
  self-correct; a silent failure derails the loop.

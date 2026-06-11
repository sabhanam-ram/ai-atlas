---
slug: rag
display_name: Retrieval-Augmented Generation (RAG)
---

**Retrieval-Augmented Generation (RAG)** is a pattern where a language model's
answer is grounded in documents fetched at query time from an external knowledge
source, rather than relying solely on what the model learned during training. The
retrieved passages are inserted into the prompt as context, so the model can cite
specific, up-to-date, or private information it never memorized.

## Why it exists

A model's weights are a lossy, frozen snapshot of its training data. RAG addresses
three limits of that snapshot:

- **Freshness** — knowledge changes after training ends; retrieval pulls current data.
- **Coverage** — private/proprietary corpora were never in training; retrieval reaches them.
- **Attribution** — answers can point back to source passages, reducing hallucination
  and enabling verification.

## The canonical pipeline

1. **Index** — split source documents into chunks, embed each chunk into a vector,
   and store the vectors (plus the text) in a vector index.
2. **Retrieve** — embed the user's query, find the nearest chunks by vector similarity
   (often combined with keyword/BM25 search → *hybrid retrieval*).
3. **Augment** — assemble the top chunks into the prompt as grounding context.
4. **Generate** — the model answers using the supplied context, ideally with citations.

## Key levers and failure modes

- **Chunking** strategy and size strongly affect recall and precision.
- **Re-ranking** the retrieved set with a cross-encoder improves the final context quality.
- **Retrieval quality is the ceiling**: if the right passage isn't retrieved, generation
  cannot recover it ("garbage in, garbage out").
- RAG is increasingly **agentic** — the model decides *when* and *what* to retrieve, may
  issue multiple queries, and can treat retrieval as a [tool](tool-use.html) rather than a
  fixed first step.

## Related

Closely tied to [agent memory](agent-memory.html) (a long-term memory store is usually a
retrieval store) and to [tool use](tool-use.html) (retrieval invoked as a callable tool).

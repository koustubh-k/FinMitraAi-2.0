# Research Agent Architecture

The FinMitra 2.0 Research Agent utilizes an **Evidence-First Agentic Workflow** built on `LangGraph`. 
Instead of relying on the LLM's internal weights for financial truth, the agent acts strictly as an interpreter of retrieved evidence and tool outputs.

## State Management (`ResearchState`)

The LangGraph workflow passes a strongly typed `ResearchState` object between nodes.

```python
class ResearchState(TypedDict):
    query: str
    messages: List[BaseMessage]
    retrieved_chunks: List[DocumentChunk]
    evidence: List[Evidence]
    generated_answer: Optional[str]
    citations: List[str]
    status: str
    error: Optional[str]
```

## Nodes and Workflow

1. **`analyze`**: Determines if the query requires external tools (like checking a user's portfolio) or semantic retrieval.
2. **`retrieve`**: Performs hybrid search against the pgvector database.
3. **`generate`**: Instructs the LLM to synthesize an answer strictly bound by the retrieved context.
4. **`validate`**: Extracts citations from the generated answer and maps them to the source Evidence models.

## Safety & Streaming

The agent never exposes its raw "chain of thought" to the end user. Instead, the `status` field in the state is streamed to the UI via Server-Sent Events (SSE) (e.g. "Searching financial sources...").

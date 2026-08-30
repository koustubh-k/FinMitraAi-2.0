# Phase 7 Benchmark Report

## Overview
This document captures the performance benchmarks for the FinMitra multi-agent architecture as measured during Phase 7.

## Baseline Latencies (ms)
Measurements captured against `mistral/open-mistral-7b` running via LangChain with structural parsing.

| Route       | Query Example                                | P50 (ms) | Notes                                      |
|-------------|----------------------------------------------|----------|--------------------------------------------|
| Research    | "What are the major risks facing TCS?"       | ~4920    | Retrieval + heavy reasoning + generation   |
| Portfolio   | "What is my portfolio value?"                | ~590     | Fast DB lookup + small context             |
| Education   | "Explain P/E ratio to a beginner"            | ~460     | Zero-shot explanation                      |
| General     | "Hello, how are you?"                        | ~505     | Simple acknowledgement                     |

*Note: The LLM model and network transit account for ~95% of the Research latency.*

## Identified Bottlenecks
1. **Research Agent Context Window**: Fetching dense documents and appending them directly into the context window significantly slows down Time-to-First-Token (TTFT) for the Research agent.
2. **Supervisor Sequential Routing**: The supervisor currently blocks execution until it has parsed the structured output.

## Optimizations Recommended for Production
1. **Parallel Tool Calling**: The Portfolio agent iterates sequentially up to 5 times. Transitioning to models that support parallel tool calling will drop multi-tool latency by 50%.
2. **Streaming Yield**: Currently the API awaits the full `AssistantState`. Upgrading FastAPI to yield Server-Sent Events (SSE) will drastically improve perceived performance for the end-user.

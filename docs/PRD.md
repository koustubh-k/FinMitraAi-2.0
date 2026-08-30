# FinMitra 2.0 Product Requirements Document

## 1. Product Vision
An AI-powered financial research and portfolio intelligence platform that helps users understand markets using verifiable evidence, structured analysis, and transparent AI reasoning.

## 2. Problem
Financial information is fragmented. Existing AI chatbots hallucinate facts, use outdated knowledge, hide sources, are unreliable with calculations, and don't maintain portfolio context.

## 3. Product Principles
- **Evidence first**: Every factual claim should have a source.
- **Calculation first**: Financial calculations must be deterministic Python code, not LLM generations.
- **AI second**: LLMs interpret and explain data rather than inventing it.
- **User control**: No autonomous financial transactions.
- **Transparent uncertainty**: Say "Insufficient evidence" instead of hallucinating.
- **Cost aware**: Monitor LLM costs and latency.
- **Provider agnostic**: Pluggable LLM backends.

## 4. Scope
- AI financial research
- Natural-language financial research
- Portfolio analytics
- Portfolio Q&A
- Financial education
- Research reports
- Alerts
- Evidence explorer

## 5. Phased Approach
We are executing a 9-phase roadmap (consolidated from an initial 22-phase plan). We have completed Phase 0 (Foundation) and Phase 1 (Backend + Data Foundation), and are currently wrapping up Phase 2 (Authentication + Market Data) and Phase 3 (Deterministic Financial Engine). The next major goal is Phase 4, which will introduce the AI Research MVP combining RAG, Evidence tracking, and the first LangGraph agent. Subsequent phases will introduce multi-agent orchestration, safety guardrails, and production hardening.

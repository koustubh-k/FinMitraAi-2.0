# Phase 7 Evaluation Methodology

## Overview
This document describes the automated evaluation framework instituted in Phase 7 to measure the correctness and safety of the FinMitra AI Assistant.

## Datasets
Evaluation datasets are maintained in `apps/api/evals/datasets/*.jsonl`.
- `routing.jsonl`: Tests the Supervisor Agent's ability to accurately classify user queries into one of the 4 domains (`research`, `portfolio`, `education`, `general`).

## Metrics Captured

### 1. Routing Accuracy
**Formula**: `(Correct Routes / Total Queries) * 100`
**Current Status**: **100.00% (9/9)** accuracy measured against the Mistral `open-mistral-7b` structured output endpoint.

### 2. Financial Correctness (Pending)
Tests whether the LLM faithfully translates structured DB/Engine results into natural language without hallucinating numbers.

### 3. Tool Selection Correctness (Pending)
Tests whether the agent utilizes the correct APIs given a scenario (e.g. using `get_portfolio_performance` instead of `get_asset_allocation` when asked for historical returns).

## Running Evaluations
The evaluation script can be executed locally:
```bash
cd apps/api
python -m evals.runners.run_evals
```

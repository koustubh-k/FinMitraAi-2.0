# Education Agent Architecture

The Education Agent is responsible for explaining financial concepts, terminology, and metrics.

## Prompt Strategy
The Education Agent operates primarily off its system prompt and the LLM's pre-trained knowledge base. 
It is instructed to:
1. Provide definitions, intuitions, and examples.
2. Adapt to the user's implicit expertise level.
3. Explicitly decline providing personalized financial advice or precise live market data (deferring those to the Portfolio and Research agents).

## Future Expansion
In future phases, if an educational query requires retrieving specific historical financial literature or textbook definitions, the Education Agent may be equipped with a specialized RAG tool. For Phase 5, it relies on the model's weights for general knowledge.

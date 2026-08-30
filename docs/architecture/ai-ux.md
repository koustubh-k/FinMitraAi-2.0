# FinMitra Phase 6: AI UX Architecture

## 1. Streaming Transparency
To build trust, FinMitra explicitly streams its status to the user without exposing internal "chain-of-thought" or reasoning prompts.
- **Statuses**: e.g., "Analyzing your portfolio...", "Searching financial sources...". 
- **Tool Statuses**: Standardized to `running_tool_<name>`, displayed elegantly on the UI (e.g. "Checking portfolio summary...").

## 2. Separation of Facts and Explanations
FinMitra visually distinguishes structured financial facts from AI-generated explanations.
- **Financial Result Cards**: The UI actively listens for `tool_results` stream events. When structured data (like Portfolio Value or PnL) is returned by tools, it is rendered in clean, distinct UI cards.
- **Explanations**: The LLM's natural language response sits below the data, contextualizing the facts but not calculating them.

## 3. Evidence and Citations
- **Event `citations`**: Citations are streamed as an array of document titles/identifiers.
- **Source Panel**: A dedicated "Sources & Evidence" section cleanly lists the references, ensuring the user can verify where the LLM pulled its data from.

## 4. Error Handling
- Safe error states exist. Instead of exposing raw `JSONDecodeError` or SQL failures, the frontend gracefully shows "An error occurred. Please ensure you are logged in and the service is available."
- If a tool times out, the tool card explicitly displays the timeout error cleanly in red, rather than crashing the assistant stream.

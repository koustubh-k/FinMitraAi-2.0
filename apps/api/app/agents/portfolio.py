from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from app.agents.state import AssistantState
from app.tools.financial import get_portfolio_tools
import os
import json

PORTFOLIO_PROMPT = """You are the Portfolio Agent of FinMitra, a financial AI assistant.
Your goal is to answer questions about the user's portfolio, holdings, P&L, and asset allocation.

Guidelines:
1. ALWAYS use the provided tools to retrieve financial data. Do NOT perform arithmetic or calculations yourself.
2. The user_id is automatically bound to the tools. 
3. If you need a portfolio_id, call `get_user_portfolios` first to list them.
4. Explain the structured results from the tools in simple, natural language.
5. If a tool returns an error, gracefully inform the user.
6. Do NOT provide personalized financial advice (e.g. "You should sell this stock"). You may only explain the current state of their portfolio.
"""

def handle_portfolio(state: AssistantState) -> AssistantState:
    """Handle portfolio queries using tools."""
    state["status"] = "analyzing_portfolio"
    
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    # We use LangChain's built-in tool calling capabilities
    llm = _get_tool_llm(provider)
    if not llm:
        state["generated_answer"] = "Error: LLM provider not configured properly."
        return state
        
    tools = get_portfolio_tools(state["user_id"])
    llm_with_tools = llm.bind_tools(tools)
    
    # Simple loop for tool execution
    messages = [SystemMessage(content=PORTFOLIO_PROMPT), HumanMessage(content=state["query"])]
    tool_results = []
    
    for _ in range(5):  # Max 5 iterations to prevent infinite loops
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        if not hasattr(response, "tool_calls") or not response.tool_calls:
            state["generated_answer"] = response.content
            state["tool_results"] = tool_results
            return state
            
        for tool_call in response.tool_calls:
            state["status"] = f"running_tool_{tool_call['name']}"
            # Find the tool
            tool_instance = next((t for t in tools if t.name == tool_call["name"]), None)
            if tool_instance:
                try:
                    result = tool_instance.invoke(tool_call["args"])
                    tool_results.append({tool_call["name"]: result})
                    # Add tool result to messages
                    messages.append(ToolMessage(
                        content=json.dumps(result),
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"]
                    ))
                except Exception as e:
                    messages.append(ToolMessage(
                        content=f"Error: {str(e)}",
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"]
                    ))
            else:
                messages.append(ToolMessage(
                    content="Error: Tool not found.",
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"]
                ))

    state["generated_answer"] = "I had to stop analyzing because it took too many steps. Please try a simpler query."
    return state

def _get_tool_llm(provider: str):
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model=os.getenv("LLM_MODEL", "llama3-8b-8192"))
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=os.getenv("LLM_MODEL", "gemini-1.5-flash"))
    elif provider == "openrouter":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model=os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct:free")
        )
    else: # Default OpenAI
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-4o-mini"))

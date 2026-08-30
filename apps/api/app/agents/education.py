from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import AssistantState
import os

EDUCATION_PROMPT = """You are the Education Agent of FinMitra, a financial AI assistant.
Your goal is to explain financial concepts, terminology, formulas, and investment mechanics.

Guidelines:
1. Explain concepts clearly. Adapt your explanation level (beginner, intermediate, advanced) based on the user's implicit or explicit request.
2. Structure your response logically. Use: Definition, Intuition, Example, Interpretation, and common Misconceptions where helpful.
3. Focus on education. Do NOT provide personalized financial advice (e.g. "You should buy this").
4. If the user asks about specific company metrics (like "What is TCS's P/E?"), provide the explanation of the metric, but if you don't know the exact current number, state that you are an education agent and don't have real-time market data access, but explain what a high or low number would mean for them.
"""

def handle_education(state: AssistantState) -> AssistantState:
    """Handle educational financial queries."""
    state["status"] = "explaining"
    
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    llm = _get_llm(provider)
    
    messages = [
        SystemMessage(content=EDUCATION_PROMPT),
        HumanMessage(content=state["query"])
    ]
    
    if llm:
        response = llm.invoke(messages)
        state["generated_answer"] = response.content
    else:
        state["generated_answer"] = "Error: LLM provider not configured properly."
        
    return state

def _get_llm(provider: str):
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

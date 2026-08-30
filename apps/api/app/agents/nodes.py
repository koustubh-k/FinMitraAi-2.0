from app.agents.state import AssistantState
from app.retrieval.search import SearchService
from app.retrieval.reranker import rerank_results
from app.db.session import SessionLocal
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.prompts import SYSTEM_PROMPT
import os

def analyze_query(state: AssistantState) -> AssistantState:
    """Analyze query to decide if we need retrieval, tools, or both."""
    # Simple heuristic for MVP: always retrieve
    state["status"] = "analyzing_query"
    return state

def retrieve(state: AssistantState) -> AssistantState:
    """Retrieve documents from vector store."""
    state["status"] = "retrieving_evidence"
    
    db = SessionLocal()
    try:
        search_service = SearchService(db)
        # 1. Hybrid Search
        results = search_service.hybrid_search(state["query"], top_k=5)
        # 2. Rerank
        reranked = rerank_results(state["query"], results, top_k=3)
        
        state["retrieved_chunks"] = reranked
        # In a full app, we would map chunks to Evidence models here
        # For MVP, we just pass the text
    finally:
        db.close()
        
    return state

def generate_answer(state: AssistantState) -> AssistantState:
    """Generate final answer using the LLM and retrieved evidence."""
    state["status"] = "generating_answer"
    
    evidence_text = "\n\n".join([f"Source {c.document.title if c.document else 'Unknown'}:\n{c.text}" for c in state.get("retrieved_chunks", [])])
    
    prompt = SYSTEM_PROMPT.format(evidence=evidence_text)
    
    messages = [SystemMessage(content=prompt), HumanMessage(content=state["query"])]
    
    # We will instantiate the LLM here dynamically based on the .env provider settings
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    # Simple abstraction for MVP
    llm = _get_llm(provider)
    
    if llm:
        response = llm.invoke(messages)
        state["generated_answer"] = response.content
    else:
        state["generated_answer"] = "Error: LLM provider not configured properly."
        
    return state

def validate_citations(state: AssistantState) -> AssistantState:
    """Ensure answer has proper citations."""
    state["status"] = "validating_citations"
    # Basic MVP implementation
    state["citations"] = [c.document.title for c in state.get("retrieved_chunks", []) if c.document]
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

from langgraph.graph import StateGraph, END
from app.agents.state import AssistantState
from app.agents.supervisor import route_query
from app.agents.nodes import analyze_query, retrieve, generate_answer, validate_citations
from app.agents.portfolio import handle_portfolio
from app.agents.education import handle_education

def route_decision(state: AssistantState) -> str:
    """Returns the next node based on the supervisor's route."""
    route = state.get("route", "general")
    if route == "research":
        return "research_analyze"
    elif route == "portfolio":
        return "portfolio"
    elif route == "education":
        return "education"
    else:
        return "general"

def handle_general(state: AssistantState) -> AssistantState:
    """Fallback for simple greetings or unknown queries."""
    state["status"] = "complete"
    state["generated_answer"] = "I am FinMitra, your financial assistant. I can help you with portfolio analysis, financial research, and education."
    return state

def build_graph():
    """Builds and compiles the Multi-Agent Assistant LangGraph."""
    workflow = StateGraph(AssistantState)
    
    # Add nodes
    workflow.add_node("supervisor", route_query)
    workflow.add_node("general", handle_general)
    workflow.add_node("portfolio", handle_portfolio)
    workflow.add_node("education", handle_education)
    
    # Research Subgraph Nodes
    workflow.add_node("research_analyze", analyze_query)
    workflow.add_node("research_retrieve", retrieve)
    workflow.add_node("research_generate", generate_answer)
    workflow.add_node("research_validate", validate_citations)
    
    # Add edges
    workflow.set_entry_point("supervisor")
    
    # Conditional edge from supervisor
    workflow.add_conditional_edges("supervisor", route_decision, {
        "research_analyze": "research_analyze",
        "portfolio": "portfolio",
        "education": "education",
        "general": "general"
    })
    
    # Research subgraph edges
    workflow.add_edge("research_analyze", "research_retrieve")
    workflow.add_edge("research_retrieve", "research_generate")
    workflow.add_edge("research_generate", "research_validate")
    workflow.add_edge("research_validate", END)
    
    # Terminal edges
    workflow.add_edge("portfolio", END)
    workflow.add_edge("education", END)
    workflow.add_edge("general", END)
    
    return workflow.compile()

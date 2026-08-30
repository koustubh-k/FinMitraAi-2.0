from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from app.agents.state import ResearchState
from app.agents.graph import build_graph
import json
import asyncio

router = APIRouter()

class ResearchRequest(BaseModel):
    query: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In a real app we wouldn't build the graph on every request, but this is an MVP
agent_workflow = build_graph()

@router.post("/")
async def run_research(request: ResearchRequest):
    """
    Stream research agent status and final response using SSE.
    Provides safe events like 'analyzing_query' without exposing raw LLM thoughts.
    """
    async def event_generator():
        state = ResearchState(
            query=request.query, 
            messages=[],
            retrieved_chunks=[],
            evidence=[],
            generated_answer=None,
            citations=[],
            status="starting",
            error=None
        )
        
        # Simulate an async generator for the workflow steps
        # In a true LangGraph setup, we would use workflow.astream()
        # but for this MVP mock, we just yield the states
        
        # We can run the compiled graph
        for event in agent_workflow.stream(state):
            for key, val in event.items():
                if "status" in val:
                    yield {
                        "event": "status",
                        "data": json.dumps({"status": val["status"]})
                    }
        
        # Get final state
        final_state = agent_workflow.invoke(state)
        
        yield {
            "event": "complete",
            "data": json.dumps({
                "answer": final_state.get("generated_answer"),
                "citations": final_state.get("citations", [])
            })
        }
        
    return EventSourceResponse(event_generator())

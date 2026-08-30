from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from app.agents.state import AssistantState
from app.agents.graph import build_graph
from app.auth.dependencies import get_current_user
from app.models.user import User
import json
import asyncio

router = APIRouter()

class AssistantRequest(BaseModel):
    query: str

agent_workflow = build_graph()

@router.post("/chat")
async def run_assistant(
    request: AssistantRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Unified Assistant API. Routes query, analyzes portfolio, fetches market data,
    or runs RAG based on the request. Requires authentication to bind user_id to tools securely.
    """
    async def event_generator():
        # Inject the authenticated user ID into the state
        state = AssistantState(
            user_id=str(current_user.id),
            query=request.query, 
            messages=[],
            route=None,
            retrieved_chunks=[],
            evidence=[],
            tool_results=[],
            generated_answer=None,
            citations=[],
            status="starting",
            error=None
        )
        
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
                "citations": final_state.get("citations", []),
                "route": final_state.get("route", "unknown")
            })
        }
        
    return EventSourceResponse(event_generator())

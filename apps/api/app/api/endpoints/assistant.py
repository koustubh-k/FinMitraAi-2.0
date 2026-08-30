from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from app.agents.state import AssistantState
from app.agents.graph import build_graph
from app.auth.dependencies import get_current_user
from app.models.user import User
import json
import asyncio
from app.api.middleware import limiter

router = APIRouter()

class AssistantRequest(BaseModel):
    query: str

agent_workflow = build_graph()

@router.post("/chat")
@limiter.limit("10/minute")
async def run_assistant(
    request: Request,
    body: AssistantRequest,
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
            query=body.query, 
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
        
        # We can run the compiled graph with recursion limits for safety
        config = {"recursion_limit": 10}
        
        last_yielded_tool_results = []
        last_yielded_citations = []

        for event in agent_workflow.stream(state, config=config):
            for key, val in event.items():
                if "status" in val:
                    yield {
                        "event": "status",
                        "data": json.dumps({"status": val["status"]})
                    }
                if "tool_results" in val and val["tool_results"] != last_yielded_tool_results:
                    last_yielded_tool_results = val["tool_results"].copy()
                    yield {
                        "event": "tool_results",
                        "data": json.dumps(val["tool_results"])
                    }
                if "citations" in val and val["citations"] != last_yielded_citations:
                    last_yielded_citations = val["citations"].copy()
                    yield {
                        "event": "citations",
                        "data": json.dumps(val["citations"])
                    }
        
        # Get final state
        final_state = agent_workflow.invoke(state, config=config)
        
        yield {
            "event": "complete",
            "data": json.dumps({
                "answer": final_state.get("generated_answer"),
                "citations": final_state.get("citations", []),
                "route": final_state.get("route", "unknown")
            })
        }
        
    return EventSourceResponse(event_generator())

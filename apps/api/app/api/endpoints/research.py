# This module is deprecated since Phase 5.
# All research queries are now routed through the unified Assistant endpoint via the Supervisor agent.
# This file is kept as a stub to prevent import errors during transition.
# Use /api/v1/assistant/chat instead.

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def research_deprecated():
    """
    DEPRECATED: Use /api/v1/assistant/chat instead.
    Research queries are now handled by the Supervisor-routed multi-agent graph.
    """
    return {"message": "This endpoint is deprecated. Use /api/v1/assistant/chat instead."}

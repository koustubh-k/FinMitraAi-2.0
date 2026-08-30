from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from app.models.document_chunk import DocumentChunk
from app.models.evidence import Evidence

class AssistantState(TypedDict):
    """
    State for the Multi-Agent Assistant.
    """
    user_id: str
    query: str
    messages: List[BaseMessage]
    route: Optional[str]
    retrieved_chunks: List[DocumentChunk]
    evidence: List[Evidence]
    tool_results: List[Dict[str, Any]]
    generated_answer: Optional[str]
    citations: List[str]
    status: str  # For streaming state to the frontend safely
    error: Optional[str]


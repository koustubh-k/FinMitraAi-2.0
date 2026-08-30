from typing import List
from app.models.document_chunk import DocumentChunk

def rerank_results(query: str, results: List[DocumentChunk], top_k: int = 3) -> List[DocumentChunk]:
    """
    Stub for a reranking pipeline (e.g., Cohere Rerank or CrossEncoder).
    Currently just returns the top_k from the existing vector search.
    """
    return results[:top_k]

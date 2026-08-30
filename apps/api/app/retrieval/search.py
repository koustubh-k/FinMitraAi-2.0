from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.document_chunk import DocumentChunk
from app.retrieval.embeddings import get_embedding_model

class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.embeddings = get_embedding_model()

    def vector_search(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        """Performs semantic search using pgvector."""
        query_vector = self.embeddings.embed_query(query)
        # Using L2 distance operator <->
        return self.db.query(DocumentChunk).order_by(
            DocumentChunk.embedding.l2_distance(query_vector)
        ).limit(top_k).all()

    def hybrid_search(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        """
        In a full production environment, this would combine vector search with
        BM25 or full-text search. For this MVP, we fall back to vector search.
        """
        return self.vector_search(query, top_k)

# Retrieval-Augmented Generation (RAG) Architecture

FinMitra 2.0 uses a robust RAG pipeline backed by PostgreSQL and `pgvector`.

## Ingestion Pipeline

Documents (PDFs, HTML) are ingested via LangChain document loaders.
1. Text is split using `RecursiveCharacterTextSplitter`.
2. Content is hashed via SHA-256 to prevent duplicate document ingestion.
3. Chunks are embedded using `text-embedding-3-small` (or equivalent open models) and stored in the `document_chunks` table as a `VECTOR(1536)` type.

## Database Models

- **`Document`**: Represents the root file (e.g., a 10-K filing) along with its metadata and content hash.
- **`DocumentChunk`**: A slice of the document text and its pgvector embedding.
- **`Evidence`**: When a chunk is used to answer a query, an Evidence record is created linking the specific chunk, the document, and the generated response.

## Retrieval Strategy

The search pipeline combines:
1. **Semantic Search**: L2 distance (`<->`) on the `pgvector` index.
2. **Keyword Search**: Standard full-text search (Planned for future phases).
3. **Reranking**: An abstraction for applying cross-encoders (e.g., Cohere) to the top K results to improve relevancy.

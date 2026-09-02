import os
from typing import List
from pathlib import Path
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.retrieval.embeddings import get_embedding_model

def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

def ingest_document(file_path: str, db: Session, source_url: str = None, title: str = None) -> Document:
    """Ingests a document (PDF, TXT, CSV) into the database."""
    ext = file_path.lower().split('.')[-1]
    
    if ext == 'pdf':
        loader = PyPDFLoader(file_path)
    elif ext == 'txt':
        loader = TextLoader(file_path, encoding='utf-8')
    elif ext == 'csv':
        loader = CSVLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
        
    pages = loader.load()
    
    # Simple hash for content deduplication
    content = "".join([p.page_content for p in pages])
    import hashlib
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # Check if exists
    existing_doc = db.query(Document).filter(Document.content_hash == content_hash).first()
    if existing_doc:
        return existing_doc
    
    doc = Document(
        title=title or Path(file_path).name,
        source="local_file",
        source_url=source_url,
        document_type=ext,
        content_hash=content_hash
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    splitter = get_text_splitter()
    chunks = splitter.split_documents(pages)
    
    embeddings = get_embedding_model()
    texts = [c.page_content for c in chunks]
    vectors = embeddings.embed_documents(texts)
    
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        doc_chunk = DocumentChunk(
            document_id=doc.id,
            chunk_index=i,
            text=chunk.page_content,
            embedding=vector,
            metadata_=chunk.metadata
        )
        db.add(doc_chunk)
    
    db.commit()
    return doc

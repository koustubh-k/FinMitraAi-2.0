import os
import tempfile
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.auth.dependencies import get_current_user
from app.retrieval.ingestion import ingest_document

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user = Depends(get_current_user),
):
    """
    Upload a document (PDF, TXT, CSV) to the RAG pipeline.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    ext = file.filename.lower().split('.')[-1]
    if ext not in ['pdf', 'txt', 'csv']:
        raise HTTPException(status_code=400, detail="Unsupported file format. Must be pdf, txt, or csv.")
        
    try:
        # Create a temporary file to save the upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            
        # Run ingestion
        doc = ingest_document(temp_path, db, source_url=file.filename, title=file.filename)
        
        # Clean up
        os.unlink(temp_path)
        
        return {
            "id": str(doc.id),
            "title": doc.title,
            "document_type": doc.document_type,
            "status": "success"
        }
    except Exception as e:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

app = FastAPI(
    title="FinMitra 2.0 API",
    description="Evidence-first financial intelligence platform API",
    version="0.1.0"
)

from sqlalchemy.exc import SQLAlchemyError


@app.get("/health")
def health_check(db: Session = Depends(get_db)):  # noqa: B008
    """Health check endpoint, verifies database connectivity."""
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db_status = "error"
        
    return JSONResponse(content={
        "status": "ok",
        "database": db_status
    }, status_code=200 if db_status == "ok" else 503)

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.router import api_router
from app.core.config import settings
from app.db.session import get_db

app = FastAPI(
    title=settings.app_name,
    description="Backend API for FinMitra",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")

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

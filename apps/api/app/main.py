from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="FinMitra 2.0 API",
    description="Evidence-first financial intelligence platform API",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return JSONResponse(content={"status": "ok"})

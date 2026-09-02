from fastapi import APIRouter

from app.api.endpoints import auth, market_data, portfolios, users, research, assistant, documents

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(portfolios.router, prefix="/portfolios", tags=["Portfolios"])
api_router.include_router(market_data.router, prefix="/market", tags=["Market Data"])
api_router.include_router(research.router, prefix="/research", tags=["Research"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])

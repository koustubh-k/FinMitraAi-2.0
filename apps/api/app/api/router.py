from fastapi import APIRouter

from app.api.endpoints import auth, market_data, portfolios, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(portfolios.router, prefix="/portfolios", tags=["Portfolios"])
api_router.include_router(market_data.router, prefix="/market", tags=["Market Data"])

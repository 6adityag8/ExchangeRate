from fastapi import APIRouter

from app.api.endpoints import convert, currencies, historical, latest

api_router = APIRouter()
api_router.include_router(convert.router, tags=["convert"])
api_router.include_router(currencies.router, prefix="/currencies", tags=["currencies"])
api_router.include_router(historical.router, prefix="/historical", tags=["historical"])
api_router.include_router(latest.router, prefix="/latest", tags=["latest"])

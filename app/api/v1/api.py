from fastapi import APIRouter
from app.api.v1.endpoints import health, video


api_router = APIRouter()

api_router.include_router(health.router, prefix="/system", tags=["system"])
api_router.include_router(video.router, prefix="/video", tags=["video"])

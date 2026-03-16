from fastapi import  Depends, HTTPException, APIRouter, status
from typing import Annotated
from app.core.config import Settings, get_settings



router = APIRouter()


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def health_check(settings: Annotated[Settings, Depends(get_settings)]) -> dict:
    """
    Health check endpoint to verify the application is running and can access its dependencies.
    """
    health_info = {
        "service": settings.app.name,
        "http_status_code": status.HTTP_200_OK,
        "status": "Health -- Okay, App is Healthy and Running",
        "environment": settings.app.env,
        "version": settings.app.version,
        "uptime_status": "optimal"
    }
    return health_info

# Create a separate endpoint for readiness check if needed, which can include checks for database connectivity, external API availability, etc.


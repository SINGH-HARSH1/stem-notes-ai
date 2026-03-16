import aiohttp
import logging
import uvicorn
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.router import router as main_router
from app.core.config import settings
from app.core.database import Base, engine
from app.models.video_task import VideoTask

__all__ = ["Base", "VideoTask"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code can be added here (e.g., connect to databases, initialize resources)
    print(f"Starting up the {settings.app.name} app...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session =  aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=settings.app.timeout))
    app.state.client_session = session
    try:
        yield
    finally:
        # Shutdown code can be added here (e.g., close database connections, clean up resources)
        print("Shutting down the STEM-Notes AI API...")
        await session.close()

app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    version=settings.app.version,
    lifespan=lifespan
)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Enable CORS for frontend or browser extension connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)


@app.get("/")
async def root():
    return {
        "message": "STEM-Notes AI API is online",
        "status": "active",
        "docs": "/docs"
    }

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.app.host, port=settings.app.port, log_level=settings.app.log_level, workers=settings.api.workers)

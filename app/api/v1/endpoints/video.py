from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.videos import VideoIngestRequest, VideoIngestResponse, VideoStatusTaskOut
from app.utils.generic_methods import generate_unique_id
from app.core.database import get_db
from app.models.video_task import VideoTask
from typing import Annotated
from app.db.database_crud.crud import fetch_video_details_by_id, create_video_task
from app.services.video_processor import process_video_lifecycle


router = APIRouter()
AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED, response_model=VideoIngestResponse)
async def ingest_video(request: VideoIngestRequest, db: AsyncSessionDep, bg_tasks: BackgroundTasks):

    video_processing_task_id = generate_unique_id("task_")
    await create_video_task(db=db, task_id=video_processing_task_id, url=request.url, depth=request.depth.value)

    bg_tasks.add_task(process_video_lifecycle,
                      video_processing_task_id,
                      request.url,
                      request.depth.value)

    response = VideoIngestResponse(
        message = "Video Processing Task Request Received, Processing--Notes Generation Started",
        video_processing_task_id = str(video_processing_task_id),
        youtube_url=request.url,
        depth=request.depth.value,
        status = "PENDING"
    )
    return response


@router.get("/status/{task_id}", response_model=VideoStatusTaskOut)
async def get_video_status(task_id: str, db: AsyncSessionDep):
    video_processing_details = await fetch_video_details_by_id(db=db, video_id=task_id)

    if video_processing_details is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video Processing Task Not Found")
    # return VideoStatusTaskOut(
    #     video_processing_task_id=video_processing_details.id,
    #     youtube_url=video_processing_details.url,
    #     depth=video_processing_details.depth,
    #     status=video_processing_details.status,
    #     message="Task details retrieved successfully"
    # )
    return video_processing_details






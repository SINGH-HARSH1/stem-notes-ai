from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.video_task import VideoTask
from sqlalchemy import select
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def create_video_task(db: AsyncSession, task_id: str, url: str, depth: str) -> VideoTask:
    """
        Creates and persists a new VideoTask record.
        Returns the newly created VideoTask object.
    """
    new_task = VideoTask(id=task_id, url=url, depth=depth)
    try:
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while creating task {task_id}: {e}")
        raise

async def update_task_status(db: AsyncSession, task_id: str, status: str):
    """
        Updates the status of an existing VideoTask by its ID.
        Commits the change if the task is found.
    """
    try:
        stmt = select(VideoTask).where(VideoTask.id == task_id)
        result = await db.execute(stmt)
        task = result.scalar_one_or_none()
        if task:
            task.status = status
            await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Failed to update task {task_id}: {e}")
        raise

async def fetch_video_details_by_id(db: AsyncSession, video_id: str) -> Optional[VideoTask]:
    """
        Fetches the complete VideoTask record for a given video_id.
        Returns the VideoTask object or None if not found.
    """
    try:
        stmt = select(VideoTask).where(VideoTask.id == video_id)
        result = await db.execute(stmt)
        video_task = result.scalar_one_or_none()
        return video_task
    except SQLAlchemyError as e:
        logger.error(f"Error fetching video {video_id}: {e}")
        return None
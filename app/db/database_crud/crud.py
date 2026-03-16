from sqlalchemy.ext.asyncio import AsyncSession
from app.models.video_task import VideoTask
from sqlalchemy import select
from typing import Optional


async def fetch_video_details_by_id(db: AsyncSession, video_id: str) -> Optional[VideoTask]:
    """
        Fetches the complete VideoTask record for a given video_id.
        Returns the VideoTask object or None if not found.
        """
    stmt = select(VideoTask).where(VideoTask.id == video_id)
    result = await db.execute(stmt)
    video_task = result.scalar_one_or_none()
    return video_task
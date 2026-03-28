from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from app.core.database import Base
import datetime
from typing import Optional

class VideoTask(Base):
    __tablename__="video_tasks"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    depth: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="PENDING")

    transcript_source: Mapped[Optional[str]] = mapped_column(String)
    raw_transcript: Mapped[Optional[str]] = mapped_column(String)
    generated_notes: Mapped[Optional[str]] = mapped_column(String)
    failure_reason: Mapped[Optional[str]] = mapped_column(String)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

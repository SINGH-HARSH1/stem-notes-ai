from pydantic import BaseModel, Field, field_validator
from enum import Enum
from urllib.parse import urlparse, parse_qs
from pydantic import ConfigDict


class SummaryDepth(str, Enum):
    BRIEF = "brief"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


class VideoIngestRequest(BaseModel):
    url : str = Field(..., description="The URL of the video to ingest")
    depth: SummaryDepth = Field(description="The summary depth of the video to be generated", default=SummaryDepth.STANDARD)

    @field_validator("url")
    def validate_url(cls, url):
        allowed_domains = ['youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be']
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.lower()
        scheme = parsed_url.scheme.lower()
        if domain_name not in allowed_domains:
            raise ValueError("Invalid YouTube URL. Please provide a valid YouTube url")
        if scheme not in ["http", "https"]:
            raise ValueError("Invalid YouTube URL. Please provide a valid URL")

        video_id = None
        if domain_name == "youtu.be":
            video_id = parsed_url.path.lstrip("/")
        else:
            query_param = parse_qs(parsed_url.query)
            video_ids = query_param.get("v")
            if video_ids and len(video_ids) > 0:
                video_id = video_ids[0]
        if not video_id or len(video_id) != 11:
            raise ValueError("Invalid YouTube URL. Please provide a valid URL, Incorrect Video ID")
        return url


class VideoIngestResponse(BaseModel):
    message: str = Field(description="Message Response to User for request processing", default="Video Processing Task Request Received, Processing--Notes Generation Started")
    video_processing_task_id: str = Field(..., description="Task ID for Video Ingestion", validation_alias="id")
    youtube_url: str = Field(..., description="Youtube URL given by USer for Video Ingestion", validation_alias="url")
    depth: str = Field(..., description="Summary depth of the video to be generated")
    status: str = Field(..., description="Current Status of the video to be generated")
    generated_notes: str | None = None
    failure_reason: str | None = None

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True)


class VideoStatusTaskOut(VideoIngestResponse):
    pass




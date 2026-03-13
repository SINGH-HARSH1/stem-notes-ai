from fastapi import HTTPException, APIRouter, status
from app.schemas.videos import VideoIngestRequest
from app.utils.generic_methods import generate_unique_id


router = APIRouter()

@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest_video(request: VideoIngestRequest):
    video_processing_id = generate_unique_id("Stem_Notes_Ai_transaction_id_")
    temp_response = {
        "message": "Video Processing Request Received, Processing/Notes Generation Started",
        "task_id": str(video_processing_id),
        "youtube url": request.url,
        "depth": request.depth,
    }
    return temp_response





import asyncio
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from app.core.database import async_session
from app.db.database_crud import crud
import logging

logger = logging.getLogger(__name__)

def fetch_youtube_id(url: str) -> str:
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
    return video_id


async def get_video_transcripts(url: str) -> tuple[list, str]:
    """
    Uses asyncio.to_thread to wrap the blocking YouTube API call.
    This satisfies the 'Use asynchronous features' warning.
    """
    video_id = fetch_youtube_id(url)

    def fetch_logic():
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
            return transcript.fetch(), "MANUAL_YT_EN"
        except:
            try:
                # 2. Try Auto-Generated English
                transcript = transcript_list.find_generated_transcript(['en'])
                return transcript.fetch(), "AUTO_YT_EN"
            except:
                # 3. Fallback: Find anything and translate
                first_available = list(transcript_list)[0]
                transcript = first_available.translate('en')
                return transcript.fetch(), "AUTO_TRANSLATED_EN"

    try:
        transcript_data = await asyncio.to_thread(fetch_logic)
        return  transcript_data
    except Exception as e:
        logger.error(f"Error fetching transcript for {url}: {e}")
        raise ValueError(f"No transcripts could be extracted: {e}")


def preprocess_transcript(transcript_data: list) -> str:
    """
    Cleans the raw transcript list into a single string.
    """
    if not transcript_data:
        return ""
    formatter = TextFormatter()
    clean_text = formatter.format_transcript(transcript_data)
    return clean_text.replace('\n', ' ').strip()


async def process_video_lifecycle(task_id: str, url: str, depth: str):

    async with async_session() as db:
        try:
            await crud.update_task_status(db, task_id, "PROCESSING")

            raw_data, source = await get_video_transcripts(url)

            formatted_text = preprocess_transcript(raw_data)

            if not formatted_text:
                raise ValueError("Transcript was empty or could not be formatted.")

            # TODO: Pass 'formatted_text' to  LLM method here
            # notes = await ai_service.generate_stem_notes(formatted_text, depth)
            notes = "AI Processing disabled until next phase."

            await crud.save_task_results(db, task_id, formatted_text, source, notes)
            logger.info(f"Task {task_id} completed successfully")

        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            # Save the actual reason it failed to the DB
            await crud.update_task_status(db, task_id, "FAILED", failure_reason=str(e))

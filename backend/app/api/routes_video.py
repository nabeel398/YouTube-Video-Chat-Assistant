from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.youtube_transcript import fetch_transcript
from app.core.text_splitter import split_text
from app.core.vector_store import create_or_load_index, add_to_index
from app.core.session_manager import set_session
from app.config import settings
import traceback

router = APIRouter()

class VideoRequest(BaseModel):
    url: str
    session_id: str = "default"

@router.post("/")
async def process_video(data: VideoRequest):
    try:
        video_url = data.url
        session_id = data.session_id
        
        print(f"Processing video for session: {session_id}")
        
        # Validate video length (basic check)
        if any(domain in video_url for domain in ['youtube.com/watch', 'youtu.be']):
            print("YouTube video detected - checking potential length issues...")
        
        # Fetch transcript with timeout handling
        text = fetch_transcript(video_url)
        
        if not text:
            raise HTTPException(status_code=400, detail="No transcript found or transcript is empty")
        
        # Check if transcript is too large (rough estimate for 2+ hour videos)
        if len(text) > 100000:  # ~100K characters threshold
            print(f"Large transcript detected: {len(text)} characters")
            # You might want to split processing or warn the user
        
        # Split text into chunks
        chunks = split_text(text)
        print(f"Created {len(chunks)} chunks from transcript")
        
        # Store chunks using shared session manager
        set_session(session_id, {"chunks": chunks})
        
        # Create or load index and add chunks
        index = create_or_load_index(settings.FAISS_INDEX_PATH)
        add_to_index(chunks, index, settings.FAISS_INDEX_PATH)
        
        return {
            "message": "Video processed and indexed successfully", 
            "chunks_count": len(chunks),
            "total_characters": len(text),
            "session_id": session_id,
            "estimated_duration": "processed"  # Add this for frontend feedback
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Video processing error: {str(e)}")
        print(f"Error details: {traceback.format_exc()}")
        
        # Provide more specific error messages
        error_message = str(e)
        if "too long" in error_message.lower():
            raise HTTPException(
                status_code=400, 
                detail="This video is too long (2+ hours). Please try a shorter video or ensure it has captions."
            )
        elif "transcript" in error_message.lower() and "disabled" in error_message.lower():
            raise HTTPException(
                status_code=400,
                detail="Transcripts are disabled for this video. Please try a different video with captions enabled."
            )
        elif "not found" in error_message.lower():
            raise HTTPException(
                status_code=400,
                detail="No transcript found for this video. Please ensure the video has captions/subtitles."
            )
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Error processing video: {error_message}"
            )
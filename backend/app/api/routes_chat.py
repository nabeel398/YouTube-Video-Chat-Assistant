from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.vector_store import create_or_load_index
from app.core.rag_pipeline import generate_answer
from app.core.session_manager import get_session
from app.config import settings

# Try importing the correct function name
try:
    from app.core.efficient_groq import groq_client, ask_groq_quality
    # If this works, you have the quality version
except ImportError:
    try:
        from app.core.efficient_groq import groq_client, ask_groq_efficient as ask_groq_quality
        # If this works, you have the efficient version
    except ImportError:
        # Fallback - create a dummy function
        def ask_groq_quality(context, question):
            return "Groq client not configured properly."

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    answer: str
    used_llm: bool = True
    word_count: int
    quality: str = "high"

@router.post("/", response_model=ChatResponse)
async def chat_with_video(data: ChatRequest):
    try:
        query = data.query.strip()
        session_id = data.session_id
        
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Get session data
        session_data = get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=400, detail="Please process a video first for this session")
        
        chunks = session_data.get("chunks", [])
        if not chunks:
            raise HTTPException(status_code=400, detail="No video content available. Please process a video first.")
        
        # Load index and generate answer
        index = create_or_load_index(settings.FAISS_INDEX_PATH)
        answer = generate_answer(query, chunks, index)
        
        word_count = len(answer.split())
        
        return ChatResponse(
            answer=answer,
            used_llm=True,
            word_count=word_count,
            quality="high" if word_count <= 30 else "truncated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return ChatResponse(
            answer=f"Error: {str(e)}",
            used_llm=False,
            word_count=len(str(e).split()),
            quality="low"
        )

@router.get("/usage")
async def get_usage_stats():
    """Check Groq API usage statistics"""
    return groq_client.get_usage_stats()

@router.post("/usage/reset")
async def reset_usage_stats():
    """Reset usage statistics (for testing)"""
    groq_client.reset_usage()
    return {"message": "Usage statistics reset successfully"}

@router.get("/sessions")
async def list_active_sessions():
    """List all active sessions"""
    from app.core.session_manager import user_sessions
    return {
        "active_sessions": [
            {
                "session_id": session_id,
                "chunks_count": len(data.get("chunks", [])),
                "has_data": len(data.get("chunks", [])) > 0
            }
            for session_id, data in user_sessions.items()
        ]
    }
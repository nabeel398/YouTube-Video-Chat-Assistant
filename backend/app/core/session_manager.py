# Shared session storage for the entire application
user_sessions = {}

def get_session(session_id: str):
    """Get session data by session ID"""
    return user_sessions.get(session_id)

def set_session(session_id: str, data: dict):
    """Set session data for a session ID"""
    user_sessions[session_id] = data
    print(f"Session '{session_id}' stored with data keys: {list(data.keys())}")

def delete_session(session_id: str):
    """Delete a session"""
    if session_id in user_sessions:
        del user_sessions[session_id]

def list_sessions():
    """List all active sessions (for debugging)"""
    return {
        "active_sessions": list(user_sessions.keys()),
        "session_details": {
            k: {"chunks_count": len(v.get("chunks", [])) if isinstance(v, dict) else "invalid"} 
            for k, v in user_sessions.items()
        }
    }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_video import router as video_router
from app.api.routes_chat import router as chat_router
from app.api.routes_export import router as export_router
from app.config import settings

app = FastAPI(title="YouTube Chat Assistant", debug=settings.DEBUG)

# Configure CORS properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js default port
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_router, prefix="/api/video", tags=["video"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(export_router, prefix="/api/export", tags=["export"])

@app.get("/")
async def root():
    return {"message": "YouTube Chat Assistant API Running 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "port": 8000}
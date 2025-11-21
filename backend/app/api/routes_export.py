from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.utils.pdf_generator import generate_chat_pdf

router = APIRouter()

@router.post("/export-pdf")
async def export_chat_pdf(chat: list[dict]):
    pdf_buffer = generate_chat_pdf(chat)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=chat_notes.pdf"},
    )

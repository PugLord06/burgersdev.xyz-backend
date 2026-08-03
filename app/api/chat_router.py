from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.services.rag_service import stream_chat_response
from app.api.dependencies import limiter

router = APIRouter()

@router.post("/chat")
@limiter.limit("5/minute")
async def chat_endpoint(request: Request, chat_req: ChatRequest):
    text = chat_req.get_text()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query string cannot be empty."
        )
    return StreamingResponse(
        stream_chat_response(text),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationHistoryResponse,
)
from app.core.exceptions import NotFoundError
from app.dependencies import get_db
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=ChatMessageResponse)
def send_chat_message(payload: ChatMessageRequest, db: Session = Depends(get_db)):
    service = ChatService(db)
    try:
        return service.process_message(
            lead_id=payload.lead_id,
            message=payload.message,
            channel=payload.channel,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/history/{lead_id}", response_model=ConversationHistoryResponse)
def get_chat_history(lead_id: int, db: Session = Depends(get_db)):
    service = ChatService(db)
    try:
        return service.get_conversation_history(lead_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
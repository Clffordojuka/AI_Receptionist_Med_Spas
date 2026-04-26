from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.schemas.messaging import (
    SMSOutboundRequest,
    SMSOutboundResponse,
    SMSWebhookResponse,
)
from app.core.exceptions import IntegrationError, NotFoundError
from app.dependencies import get_db
from app.services.messaging_service import MessagingService

router = APIRouter(prefix="/messaging", tags=["Messaging"])


@router.post("/sms/send", response_model=SMSOutboundResponse, status_code=status.HTTP_201_CREATED)
def send_sms(payload: SMSOutboundRequest, db: Session = Depends(get_db)):
    service = MessagingService(db)
    try:
        return service.send_sms(
            lead_id=payload.lead_id,
            to=payload.to,
            body=payload.body,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/sms/webhook", response_model=SMSWebhookResponse)
def receive_sms_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(get_db),
):
    service = MessagingService(db)
    try:
        result = service.handle_incoming_sms(
            from_number=From,
            body=Body,
        )
        return {
            "status": result["status"],
            "lead_id": result["lead_id"],
            "incoming_from": result["incoming_from"],
            "assistant_message": result["assistant_message"],
        }
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
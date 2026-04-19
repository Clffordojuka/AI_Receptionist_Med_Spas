from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.faq import FAQCreate, FAQResponse
from app.dependencies import get_db
from app.services.faq_service import FAQService

router = APIRouter(prefix="/faqs", tags=["FAQs"])


@router.post("", response_model=FAQResponse)
def create_faq(payload: FAQCreate, db: Session = Depends(get_db)):
    service = FAQService(db)
    return service.create_faq(payload)
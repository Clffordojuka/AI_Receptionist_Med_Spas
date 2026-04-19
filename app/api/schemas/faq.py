from pydantic import BaseModel


class FAQCreate(BaseModel):
    question: str
    answer: str
    category: str | None = None
    active: bool = True


class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    category: str | None = None
    active: bool

    model_config = {
        "from_attributes": True
    }
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FAQCreate(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    answer: str = Field(min_length=5, max_length=5000)
    is_published: bool = True


class FAQUpdate(BaseModel):
    question: str | None = Field(default=None, min_length=5, max_length=500)
    answer: str | None = Field(default=None, min_length=5, max_length=5000)
    is_published: bool | None = None


class FAQRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question: str
    answer: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
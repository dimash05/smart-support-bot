from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import TicketStatus


class TicketCreate(BaseModel):
    category: str = Field(min_length=2, max_length=100)
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10, max_length=5000)


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    category: str
    title: str
    description: str
    status: str
    admin_response: str | None
    created_at: datetime
    updated_at: datetime
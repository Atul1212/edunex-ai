from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# --- Email Request ---
class EmailRequest(BaseModel):
    recipient: str
    subject: str
    content: str

# --- Log Output ---
class EmailLogOut(BaseModel):
    id: UUID
    recipient: str
    subject: str
    status: str
    timestamp: datetime
    class Config:
        from_attributes = True


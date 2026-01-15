from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: str = 'STUDENT'

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True

# NEW: Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str


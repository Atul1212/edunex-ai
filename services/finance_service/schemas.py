from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date

# --- Fee Category Schemas ---
class FeeCategoryCreate(BaseModel):
    name: str
    amount: float
    description: Optional[str] = None

class FeeCategoryOut(BaseModel):
    id: UUID
    name: str
    amount: float
    description: Optional[str]
    class Config:
        from_attributes = True

# --- Payment Schemas ---
class PaymentCreate(BaseModel):
    student_id: UUID
    category_id: UUID
    amount_paid: float

class PaymentOut(BaseModel):
    id: UUID
    student_id: UUID
    amount_paid: float
    payment_date: date  # FIXED: Changed from 'date' to 'payment_date'
    status: str
    class Config:
        from_attributes = True


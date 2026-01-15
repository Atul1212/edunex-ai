from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

# --- FEE STRUCTURE ---
# Example: Tuition Fee for Class 10 = 5000
class FeeCategory(Base):
    __tablename__ = 'fee_categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)  # e.g., 'Annual Tuition'
    amount = Column(Float, nullable=False) # e.g., 50000.0
    description = Column(String, nullable=True)

# --- PAYMENT HISTORY ---
# Example: Student X paid 10000 on Date Y
class PaymentRecord(Base):
    __tablename__ = 'payments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), nullable=False) # Linked to Academic Service
    category_id = Column(UUID(as_uuid=True), ForeignKey('fee_categories.id'), nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, default=func.current_date())
    status = Column(String, default='SUCCESS') # SUCCESS/FAILED


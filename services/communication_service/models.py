from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

class EmailLog(Base):
    __tablename__ = 'email_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipient = Column(String, nullable=False)  # Student Email
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, default='SENT')
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


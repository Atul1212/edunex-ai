from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

# --- EXAM DETAILS ---
# Example: Math Final Exam, Max Marks 100
class Exam(Base):
    __tablename__ = 'exams'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)   # e.g., 'Mid-Term Physics'
    course_id = Column(UUID(as_uuid=True), nullable=False) # Linked to Academic Service
    date = Column(Date, nullable=False)
    total_marks = Column(Integer, default=100)

# --- STUDENT MARKS ---
# Example: Student A got 85 in Math Final
class Result(Base):
    __tablename__ = 'results'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_id = Column(UUID(as_uuid=True), ForeignKey('exams.id'), nullable=False)
    student_id = Column(UUID(as_uuid=True), nullable=False) # Linked to Academic Service
    marks_obtained = Column(Float, nullable=False)
    remarks = Column(String, nullable=True) # e.g., 'Good effort'


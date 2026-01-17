from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date

# --- Exam Schemas ---
class ExamCreate(BaseModel):
    name: str
    course_id: UUID
    date: date
    total_marks: int = 100

class ExamOut(BaseModel):
    id: UUID
    name: str
    course_id: UUID
    date: date
    total_marks: int
    class Config:
        from_attributes = True

# --- Result Schemas ---
class ResultCreate(BaseModel):
    exam_id: UUID
    student_id: UUID
    marks_obtained: float
    remarks: Optional[str] = None

class ResultOut(BaseModel):
    id: UUID
    exam_id: UUID
    student_id: UUID
    marks_obtained: float
    remarks: Optional[str]
    class Config:
        from_attributes = True


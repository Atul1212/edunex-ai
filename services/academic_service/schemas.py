from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from datetime import date

# --- Course Schemas ---
class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CourseOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    class Config:
        from_attributes = True

# --- Student Schemas ---
class StudentProfileCreate(BaseModel):
    user_id: UUID
    roll_number: str
    address: Optional[str] = None
    course_id: Optional[UUID] = None

class StudentProfileOut(BaseModel):
    id: UUID
    user_id: UUID
    roll_number: str
    course_id: Optional[UUID]
    class Config:
        from_attributes = True

# --- NEW: Attendance Schemas ---
class AttendanceCreate(BaseModel):
    student_id: UUID
    course_id: UUID
    status: str # PRESENT/ABSENT

class AttendanceOut(BaseModel):
    id: UUID
    student_id: UUID
    date: date
    status: str
    class Config:
        from_attributes = True


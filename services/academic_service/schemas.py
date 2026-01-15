from pydantic import BaseModel
from uuid import UUID
from typing import Optional

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

# --- Student Profile Schemas ---
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


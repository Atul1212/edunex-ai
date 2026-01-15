from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

# --- EXISTING TABLES ---
class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    teacher_id = Column(UUID(as_uuid=True), nullable=True)
    description = Column(String, nullable=True)

class StudentProfile(Base):
    __tablename__ = 'student_profiles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    roll_number = Column(String, unique=True, nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=True)
    address = Column(String, nullable=True)

# --- NEW: ATTENDANCE TABLE ---
class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('student_profiles.id'), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    date = Column(Date, default=func.current_date())
    status = Column(String, nullable=False) # 'PRESENT', 'ABSENT', 'LATE'


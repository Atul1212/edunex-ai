from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

# Table for Classes/Subjects
class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False) # e.g. 'Class 10 - Math'
    teacher_id = Column(UUID(as_uuid=True), nullable=True) # ID from Auth Service
    description = Column(String, nullable=True)

# Table for Student Details
class StudentProfile(Base):
    __tablename__ = 'student_profiles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False) # Link to Auth User
    roll_number = Column(String, unique=True, nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=True)
    address = Column(String, nullable=True)


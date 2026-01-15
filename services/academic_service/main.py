from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from . import models, schemas, database

# Create Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title='EduNex Academic Service')

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def health_check():
    return {'status': 'Academic Service Running', 'port': '8002'}

# --- COURSE API ---
@app.post('/courses', response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(name=course.name, description=course.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.get('/courses', response_model=List[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

# --- STUDENT API ---
@app.post('/students', response_model=schemas.StudentProfileOut)
def create_student_profile(student: schemas.StudentProfileCreate, db: Session = Depends(get_db)):
    if db.query(models.StudentProfile).filter(models.StudentProfile.roll_number == student.roll_number).first():
        raise HTTPException(status_code=400, detail='Roll Number already registered')
    new_profile = models.StudentProfile(user_id=student.user_id, roll_number=student.roll_number, address=student.address, course_id=student.course_id)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

# --- ATTENDANCE API ---
@app.post('/attendance', response_model=schemas.AttendanceOut)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    new_record = models.Attendance(student_id=attendance.student_id, course_id=attendance.course_id, status=attendance.status)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@app.get('/attendance/{student_id}', response_model=List[schemas.AttendanceOut])
def get_student_attendance(student_id: UUID, db: Session = Depends(get_db)):
    return db.query(models.Attendance).filter(models.Attendance.student_id == student_id).all()


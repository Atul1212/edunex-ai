from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from . import models, schemas, database

# Create Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title='EduNex Exam Service')

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def health_check():
    return {'status': 'Exam Service Running', 'port': '8004'}

# --- EXAM MANAGEMENT ---
@app.post('/exams', response_model=schemas.ExamOut)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    new_exam = models.Exam(name=exam.name, course_id=exam.course_id, date=exam.date, total_marks=exam.total_marks)
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return new_exam

@app.get('/exams/course/{course_id}', response_model=List[schemas.ExamOut])
def list_exams(course_id: UUID, db: Session = Depends(get_db)):
    return db.query(models.Exam).filter(models.Exam.course_id == course_id).all()

# --- RESULT MANAGEMENT ---
@app.post('/results', response_model=schemas.ResultOut)
def add_result(result: schemas.ResultCreate, db: Session = Depends(get_db)):
    new_result = models.Result(
        exam_id=result.exam_id,
        student_id=result.student_id,
        marks_obtained=result.marks_obtained,
        remarks=result.remarks
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result

@app.get('/results/student/{student_id}', response_model=List[schemas.ResultOut])
def student_results(student_id: UUID, db: Session = Depends(get_db)):
    return db.query(models.Result).filter(models.Result.student_id == student_id).all()


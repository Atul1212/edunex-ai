from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from . import models, schemas, database

# Create Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title='EduNex Finance Service')

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def health_check():
    return {'status': 'Finance Service Running', 'port': '8003'}

# --- FEE CATEGORY API ---
@app.post('/fee-categories', response_model=schemas.FeeCategoryOut)
def create_category(category: schemas.FeeCategoryCreate, db: Session = Depends(get_db)):
    new_cat = models.FeeCategory(name=category.name, amount=category.amount, description=category.description)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@app.get('/fee-categories', response_model=List[schemas.FeeCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.FeeCategory).all()

# --- PAYMENT API ---
@app.post('/payments', response_model=schemas.PaymentOut)
def record_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    # Real world logic: Check if category exists first
    new_pay = models.PaymentRecord(
        student_id=payment.student_id,
        category_id=payment.category_id,
        amount_paid=payment.amount_paid
    )
    db.add(new_pay)
    db.commit()
    db.refresh(new_pay)
    return new_pay

@app.get('/payments/{student_id}', response_model=List[schemas.PaymentOut])
def student_history(student_id: UUID, db: Session = Depends(get_db)):
    return db.query(models.PaymentRecord).filter(models.PaymentRecord.student_id == student_id).all()


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

# Create Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title='EduNex Communication Service')

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def health_check():
    return {'status': 'Communication Service Running', 'port': '8005'}

# --- SEND EMAIL API ---
@app.post('/send-email', response_model=schemas.EmailLogOut)
def send_email(email: schemas.EmailRequest, db: Session = Depends(get_db)):
    # 1. Simulate Sending Email (Print to Console)
    print(f'\n========================================')
    print(f' SENDING EMAIL TO: {email.recipient}')
    print(f' SUBJECT: {email.subject}')
    print(f' CONTENT: {email.content}')
    print(f'========================================\n')
    
    # 2. Log to Database
    new_log = models.EmailLog(
        recipient=email.recipient,
        subject=email.subject,
        content=email.content,
        status='SENT'
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

# --- VIEW LOGS ---
@app.get('/logs', response_model=List[schemas.EmailLogOut])
def view_logs(db: Session = Depends(get_db)):
    return db.query(models.EmailLog).order_by(models.EmailLog.timestamp.desc()).all()


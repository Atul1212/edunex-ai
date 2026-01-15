from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, utils, database

# Create Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title='EduNex Auth Service')

# DB Session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def health_check():
    return {'status': 'Auth Service Running'}

@app.post('/register', response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    hashed_password = utils.get_password_hash(user.password)
    new_user = models.User(email=user.email, password_hash=hashed_password, full_name=user.full_name, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Check User
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail='Invalid Credentials')
    
    # 2. Check Password
    if not utils.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail='Invalid Credentials')
    
    # 3. Generate Token
    access_token = utils.create_access_token(data={'sub': user.email, 'role': user.role})
    return {'access_token': access_token, 'token_type': 'bearer'}


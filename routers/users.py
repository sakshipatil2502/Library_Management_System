from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import crud, schemas
from auth import get_current_admin, get_current_user, verify_password, create_access_token
from database import get_db
from typing import List
from models import User as DBUser



router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[schemas.UserOut])
def list_all_users(db: Session = Depends(get_db), admin: schemas.UserOut = Depends(get_current_admin)):
    return crud.list_users(db)

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db), admin: schemas.UserOut = Depends(get_current_admin)):
    return crud.update_user(db, user_id, user)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: schemas.UserOut = Depends(get_current_admin)):
    return crud.delete_user(db, user_id)

@router.get("/", response_model=list[schemas.UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: DBUser = Depends(get_current_admin)
):
    return crud.list_users(db)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: DBUser = Depends(get_current_admin)
):
    if current_admin.id == user_id:
        raise HTTPException(status_code=403, detail="Admin cannot delete themselves")
    return crud.delete_user(db, user_id)    

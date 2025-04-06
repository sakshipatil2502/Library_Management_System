from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
import models
from database import get_db
from auth import get_current_user, get_current_admin

router = APIRouter()

@router.post("/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), admin: schemas.UserOut = Depends(get_current_admin)):
    return crud.create_book(db, book)

@router.get("/", response_model=List[schemas.BookOut])
def get_books(
    author: Optional[str] = None,
    category: Optional[str] = None,
    available_only: bool = False,
    db: Session = Depends(get_db)
):
    return crud.list_books(db, author, category, available_only)

@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book_by_id(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/search/", response_model=List[schemas.BookOut])
def search_books(query: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_books(db, query)

@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db), admin: schemas.UserOut = Depends(get_current_admin)):
    return crud.update_book(db, book_id, book)

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), admin: schemas.UserOut = Depends(get_current_admin)):
    return crud.delete_book(db, book_id)

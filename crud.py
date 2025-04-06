from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash
from fastapi import HTTPException
from datetime import date

# User Functions
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def list_users(db: Session):
    return db.query(models.User).all()

def update_user(db: Session, user_id: int, user: schemas.UserBase):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Book Functions
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

def list_books(db: Session, author: str = None, category: str = None, available_only: bool = False):
    query = db.query(models.Book)
    if author:
        query = query.filter(models.Book.author == author)
    if category:
        query = query.filter(models.Book.category == category)
    if available_only:
        query = query.filter(models.Book.quantity > 0)
    return query.all()

def search_books(db: Session, search: str):
    return db.query(models.Book).filter(
        (models.Book.title.ilike(f"%{search}%")) |
        (models.Book.author.ilike(f"%{search}%")) |
        (models.Book.isbn.ilike(f"%{search}%"))
    ).all()

# Transaction Functions
def checkout_book(db: Session, checkout: schemas.Checkout):
    book = db.query(models.Book).filter(models.Book.id == checkout.book_id).first()
    if not book or book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    transaction = models.Transaction(**checkout.dict())
    book.quantity -= 1
    db.add(transaction)
    db.commit()
    return transaction

def return_book(db: Session, return_data: schemas.TransactionReturn):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.book_id == return_data.book_id,
        models.Transaction.user_id == return_data.user_id,
        models.Transaction.return_date == None
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    book = db.query(models.Book).filter(models.Book.id == return_data.book_id).first()
    book.quantity += 1
    transaction.return_date = return_data.return_date
    db.commit()
    return transaction

def borrowed_books(db: Session, user_id: int):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.return_date == None
    ).all()

def get_overdue_books(db: Session):
    return db.query(models.Transaction).filter(
        models.Transaction.due_date < date.today(),
        models.Transaction.return_date == None
    ).all()
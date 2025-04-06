from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from auth import get_current_user, get_current_admin
from typing import List
import models
from datetime import datetime,timedelta

router = APIRouter()

@router.post("/checkout", response_model=schemas.TransactionOut)
def checkout_book(checkout: schemas.Checkout, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.checkout_book(db, checkout)

@router.get("/", response_model=List[schemas.TransactionOut])
def get_transactions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()


# @router.post("/checkout")
# def checkout_book(checkout: schemas.Checkout, db: Session = Depends(get_db), user: schemas.UserOut = Depends(get_current_user)):
#     return crud.checkout_book(db, checkout)

# @router.post("/return")
# def return_book(return_data: schemas.Return, db: Session = Depends(get_db), user: schemas.UserOut = Depends(get_current_user)):
#     return crud.return_book(db, return_data)

@router.post("/return", response_model=schemas.TransactionOut)
def return_book(
    data: schemas.TransactionReturn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.user_id == data.user_id,
        models.Transaction.book_id == data.book_id,
        models.Transaction.return_date == None
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found or already returned")

    transaction.return_date = data.return_date
    db.commit()
    db.refresh(transaction)

    return transaction 



@router.get("/borrowed/{user_id}")
def get_borrowed_books(user_id: int, db: Session = Depends(get_db), admin: schemas.UserOut = Depends(get_current_admin)):
    return crud.borrowed_books(db, user_id)

# @router.get("/overdue")
# def get_overdue_books(db: Session = Depends(get_db), admin: schemas.UserOut = Depends(get_current_admin)):
#     return crud.overdue_books(db)

@router.get("/overdue", response_model=List[schemas.TransactionOut])
def get_overdue_books(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_overdue_books(db)


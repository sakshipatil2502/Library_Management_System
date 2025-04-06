from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    published_year: int
    category: str
    quantity: int

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookOut(BookBase):
    id: int
    class Config:
        from_attributes = True
        # orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    role: str

class UserOut(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True
        # orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Checkout(BaseModel):
    user_id: int
    book_id: int
    checkout_date: date
    due_date: date

# class Return(BaseModel):
#     user_id: int
#     book_id: int
#     return_date: date

class TransactionReturn(BaseModel):
    user_id: int
    book_id: int
    return_date: date    

class TransactionOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    checkout_date: date
    due_date: date
    return_date: Optional[date]

    class Config:
        from_attributes = True  # replaces orm_mode=True for Pydantic v2

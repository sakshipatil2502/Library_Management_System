from fastapi import FastAPI
from database import engine, Base
import models
from routers import books, users, transactions

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
def read_root():
    return {"msg": "Library Management System API is running !"}

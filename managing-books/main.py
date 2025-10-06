from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, Any
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from random import randint

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

class Book_management(BaseModel):
    book_id: int
    book_name: str
    author_name: str

class User_management(BaseModel):
    user_id: int
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(get_db)]


@app.post('/books/{book_id}', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book_management, db:db_dependencies):
    books = models.Books(**book.dict())
    db.add(books)
    db.commit()
    db.refresh(books)
    return books

@app.get("/books/", response_model=List[Book_management])
async def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Books).all()
    return books

@app.get('/books/{book_id}')
async def get_book(id: int, db:db_dependencies):
    db_post = db.query(models.Books).filter(models.Books.book_id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="book id is not found")
    return db_post

@app.put('/books/{book_id}')
async def update_books(id: int, update_book: Book_management, db: db_dependencies):
    db_book = db.query(models.Books).filter(models.Books.book_id == id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="id not found!")
    db_book.book_name = update_book.book_name
    db_book.author_name = update_book.author_name

    db.commit()
    db.refresh(db_book)

    return {"message": "book successfully updated", "book_name":db_book.book_name, "author_name": db_book.author_name}


@app.delete('/books/{bok_id}', status_code=status.HTTP_200_OK)
async def delete_book(id:int, db:db_dependencies):
    db_delete = db.query(models.Books).filter(models.Books.book_id == id).first()
    if db_delete is None:
        raise HTTPException(status_code=404, detail='Book id not found')
    db.delete(db_delete)
    return db_delete
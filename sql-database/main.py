from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# --- App Initialization ---
app = FastAPI()

# Create database tables on startup based on SQLAlchemy models
models.Base.metadata.create_all(bind=engine)


# --- Pydantic Models (Data Schemas) ---

# This model is for creating a Post, inheriting from BaseModel is correct.
class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str
    model_config = ConfigDict(from_attributes=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post('/posts/', status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db:db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get('/posts/{post_id}', status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db:db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="user not found")
    return post

@app.delete('/post/', status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db:db_dependency):
    delete_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if delete_post is None:
        raise HTTPException(status_code=404, detail="db_id is not found")
    db.delete(delete_post)
    db.commit()

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user: UserBase, db: db_dependency):

    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post('/users/{user_id}', status_code=status.HTTP_201_CREATED)
async def read_users(user_id: int, db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user

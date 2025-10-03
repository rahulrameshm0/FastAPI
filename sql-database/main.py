from fastapi import FastAPI, Depends, status
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

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user: UserBase, db: db_dependency):

    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer,primary_key=True, index=True)
    username = Column(String(150), unique=True)

class Books(Base):
    __tablename__ = 'books'
    book_name = Column(String(150))
    author_name = Column(String(150))
    book_id = Column(Integer, primary_key=True)
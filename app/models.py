from sqlalchemy import Column, Integer, String, Date
from .database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    birth_date = Column(Date)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    author_id = Column(Integer)
    available_copies = Column(Integer)


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer)
    reader_name = Column(String)
    borrow_date = Column(Date)
    return_date = Column(Date, nullable=True)

from sqlalchemy.orm import Session
from . import models, schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_borrow(db: Session, borrow: schemas.BorrowCreate):
    db_borrow = models.Borrow(**borrow.dict())
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)

    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    if book and book.available_copies > 0:
        book.available_copies -= 1
        db.commit()
        db.refresh(book)
        return db_borrow
    else:
        db.rollback()
        raise ValueError("Not enough available copies of the book")


def get_borrows(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Borrow).offset(skip).limit(limit).all()


def return_book(db: Session, borrow_id: int):
    db_borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if db_borrow and not db_borrow.return_date:
        db_borrow.return_date = date.today()
        db.commit()

        book = db.query(models.Book).filter(models.Book.id == db_borrow.book_id).first()
        book.available_copies += 1
        db.commit()
        return db_borrow
    else:
        raise ValueError("Borrow record not found or already returned")

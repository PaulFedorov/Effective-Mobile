from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas, database

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints for Authors
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db=db, skip=skip, limit=limit)

# Endpoints for Books
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)

# Endpoints for Borrows
@app.post("/borrows/", response_model=schemas.Borrow)
def create_borrow(borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_borrow(db=db, borrow=borrow)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough available copies")

@app.get("/borrows/", response_model=list[schemas.Borrow])
def read_borrows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_borrows(db=db, skip=skip, limit=limit)

@app.patch("/borrows/{borrow_id}/return", response_model=schemas.Borrow)
def return_borrow(borrow_id: int, db: Session = Depends(get_db)):
    try:
        return crud.return_book(db=db, borrow_id=borrow_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Borrow record not found or already returned")

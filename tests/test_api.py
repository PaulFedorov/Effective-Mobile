import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_author():
    response = client.post("/authors/", json={"first_name": "John", "last_name": "Doe", "birth_date": "1990-01-01"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "first_name": "John", "last_name": "Doe", "birth_date": "1990-01-01"}

def test_create_book():
    response = client.post("/books/", json={"title": "Book Title", "description": "Description", "author_id": 1, "available_copies": 5})
    assert response.status_code == 200
    assert response.json()["title"] == "Book Title"

def test_create_borrow():
    response = client.post("/borrows/", json={"book_id": 1, "reader_name": "Alice", "borrow_date": "2024-12-10"})
    assert response.status_code == 200

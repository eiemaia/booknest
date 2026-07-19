from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Book, Location

router = APIRouter(prefix="/books", tags=["Books"])

# Get all books (with optional filters)
@router.get("/")
def get_books(
    location_id: int = None,
    format: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    if location_id:
        query = query.filter(Book.location_id == location_id)
    if format:
        query = query.filter(Book.format == format)
    return query.all()

# Get a single book
@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "format": book.format,
        "location_id": book.location_id,
        "cover_url": book.cover_url
    }

# Add a new book
@router.post("/")
def create_book(
    title: str,
    author: str,
    format: str,
    location_id: int = None,
    cover_url: str = None,
    db: Session = Depends(get_db)
):
    # Validate format
    if format not in ["paperback", "hardcover", "ebook"]:
        raise HTTPException(status_code=400, detail="Format must be paperback, hardcover, or ebook")

    # Ebooks don't need a location
    if format == "ebook" and location_id:
        raise HTTPException(status_code=400, detail="Ebooks do not have a physical location")

    # Physical books need a location
    if format != "ebook" and not location_id:
        raise HTTPException(status_code=400, detail="Physical books require a location")

    # Validate location exists
    if location_id:
        location = db.query(Location).filter(Location.id == location_id).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")

    book = Book(
        title=title,
        author=author,
        format=format,
        location_id=location_id,
        cover_url=cover_url
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "format": book.format,
        "location_id": book.location_id,
        "cover_url": book.cover_url
    }

# Update a book
@router.patch("/{book_id}")
def update_book(
    book_id: int,
    title: str = None,
    author: str = None,
    format: str = None,
    location_id: int = None,
    cover_url: str = None,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if title: book.title = title
    if author: book.author = author
    if format: book.format = format
    if location_id is not None: book.location_id = location_id
    if cover_url: book.cover_url = cover_url
    db.commit()
    db.refresh(book)
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "format": book.format,
        "location_id": book.location_id,
        "cover_url": book.cover_url
    }

# Delete a book
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": f"'{book.title}' deleted"}
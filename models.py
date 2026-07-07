from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Location(Base):
    __tablename__ = "locations"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    books = relationship("Book", back_populates="location")


class Book(Base):
    __tablename__ = "books"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, nullable=False)
    author      = Column(String, nullable=False)
    cover_url   = Column(String, nullable=True)
    format      = Column(String, nullable=False)  # paperback | hardcover | ebook
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    location = relationship("Location", back_populates="books")
    loan     = relationship("Loan", back_populates="book", uselist=False)


class Loan(Base):
    __tablename__ = "loans"

    id          = Column(Integer, primary_key=True, index=True)
    book_id     = Column(Integer, ForeignKey("books.id"), nullable=False)
    friend_name = Column(String, nullable=False)
    loaned_on   = Column(String, nullable=False)
    returned_on = Column(String, nullable=True)

    book = relationship("Book", back_populates="loan")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Location

router = APIRouter(prefix="/locations", tags=["Locations"])

# Get all locations
@router.get("/")
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()

# Create a new location
@router.post("/")
def create_location(name: str, db: Session = Depends(get_db)):
    existing = db.query(Location).filter(Location.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Location already exists")
    location = Location(name=name)
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

# Delete a location
@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(location)
    db.commit()
    return {"message": f"Location '{location.name}' deleted"}
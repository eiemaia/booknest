from fastapi import FastAPI
from database import engine, Base
from routers import locations

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookNest API")

app.include_router(locations.router)

@app.get("/")
def root():
    return {"message": "Welcome to BookNest 📚"}
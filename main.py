from fastapi import FastAPI
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookNest API")

@app.get("/")
def root():
    return {"message": "Welcome to BookNest 📚"}
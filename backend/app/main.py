from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import GeneratedCode

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/codes/count")
def get_codes_count(db: Session = Depends(get_db)):
    return {"count": db.query(GeneratedCode).count()}



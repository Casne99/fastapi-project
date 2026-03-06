from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import GeneratedCode
from datetime import datetime, timedelta, timezone
from jose import jwt
from app import config

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

@app.get("/token")
def get_token():
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, "sub": "user_id"}
    token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return {"token": token}

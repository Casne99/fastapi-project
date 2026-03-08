from fastapi import FastAPI, Depends, HTTPException, status, Response
from datetime import datetime, timedelta, timezone
from jose import jwt
from . import config
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Credentials
import bcrypt

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/token")
def get_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Credentials).filter(Credentials.user == form_data.username).first()
    if not user or not bcrypt.checkpw(form_data.password.encode(), user.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
        )
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, "sub": form_data.username}
    token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
    # Imposta il cookie HttpOnly
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False  # Metti True in produzione con HTTPS
    )
    return {"message": "Login effettuato con successo"}

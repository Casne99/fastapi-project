from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import jwt
from . import config
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/token")
def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
        )
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, "sub": form_data.username}
    token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return {"token": token}

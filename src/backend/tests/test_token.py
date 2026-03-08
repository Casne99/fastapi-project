import bcrypt
import pytest
from app import config
from app.main import app
from app.models import Credentials
from fastapi.testclient import TestClient
from jose import jwt

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db(db_session):
    db_session.query(Credentials).delete()
    db_session.commit()
    password_hash = bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode()
    user = Credentials(user="admin", password=password_hash)
    db_session.add(user)
    db_session.commit()


def test_get_token_success():
    response = client.post("/api/token", data={"username": "admin", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login effettuato con successo"
    cookie = response.cookies.get("access_token")
    assert cookie is not None
    payload = jwt.decode(cookie, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    assert payload["sub"] == "admin"
    assert "exp" in payload


def test_get_token_invalid_credentials():
    response = client.post("/api/token", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Credenziali non valide"

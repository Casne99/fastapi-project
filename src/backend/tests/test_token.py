from fastapi.testclient import TestClient
from app.main import app
from app import config
from jose import jwt

client = TestClient(app)

def test_get_token_success():
    response = client.post("/token", data={"username": "admin", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    token = data["token"]
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    assert payload["sub"] == "admin"
    assert "exp" in payload

def test_get_token_invalid_credentials():
    response = client.post("/token", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Credenziali non valide"

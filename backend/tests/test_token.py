from fastapi.testclient import TestClient
from app.main import app
from app import config
from jose import jwt

client = TestClient(app)

def test_get_token():
    response = client.get("/token")
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    token = data["token"]
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    assert payload["sub"] == "user_id"
    assert "exp" in payload

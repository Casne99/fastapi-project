from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from app.main import app, get_db
from app import config
from app.models import Credentials, Base
from jose import jwt
import bcrypt
import pytest

postgres = PostgresContainer("postgres:15-alpine")


@pytest.fixture(scope="session", autouse=True)
def start_container():
    postgres.start()
    yield
    postgres.stop()


@pytest.fixture(scope="session")
def test_engine(start_container):
    url = postgres.get_connection_url().replace("postgresql://", "postgresql+psycopg2://")
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture()
def db_session(test_engine):
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestSession()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(autouse=True)
def setup_db(db_session):
    db_session.query(Credentials).delete()
    db_session.commit()
    password_hash = bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode()
    user = Credentials(user="admin", password=password_hash)
    db_session.add(user)
    db_session.commit()


@pytest.fixture(autouse=True)
def override_db(test_engine):
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def _get_test_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()


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

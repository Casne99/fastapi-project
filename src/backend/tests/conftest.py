from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from alembic.config import Config
from alembic import command
from app.main import app, get_db
import pytest
import os

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

    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", url)
    command.upgrade(alembic_cfg, "head")

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

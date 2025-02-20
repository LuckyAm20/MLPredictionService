import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from api import app
from database.database import get_session


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///testing.db", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()
    if os.path.exists("testing.db"):
        os.remove("testing.db")

@pytest.fixture(scope="function")
def session(db_engine):
    session = Session(db_engine)
    yield session
    session.close()


@pytest.fixture(scope="function")
def db_session(db_engine):
    SQLModel.metadata.drop_all(db_engine)
    SQLModel.metadata.create_all(db_engine)
    session = Session(db_engine)
    yield session
    session.close()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

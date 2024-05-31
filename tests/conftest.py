import sys
import os



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.model import Base
from main import app
from redis import Redis
from unittest.mock import MagicMock

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def get_redis():
    return MagicMock(spec=Redis)

app.dependency_overrides[get_db] = get_db
app.dependency_overrides[get_redis] = get_redis

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def authenticated_client(client):
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client
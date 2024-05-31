from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from tests.conftest import client

def test_signup(client: TestClient):
    response = client.post("/users/signup", json={"fullname": "Test User", "email": "test@example.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_signup_existing_email(client: TestClient):
    client.post("/users/signup", json={"fullname": "Test User", "email": "test2@example.com", "password": "password123"})
    response = client.post("/users/signup", json={"fullname": "Test User", "email": "test2@example.com", "password": "password123"})
    assert response.status_code == 400
    assert response.json()["message"] == "Email already registered"

def test_signup_missing_fields(client: TestClient):
    response = client.post("/users/signup", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 422  # Unprocessable Entity

def test_login(client: TestClient):
    client.post("/users/signup", json={"fullname": "Test User", "email": "testlogin@example.com", "password": "password123"})
    response = client.post("/users/session", data={"username": "testlogin@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert "access_token" in response.json()["data"]

def test_login_invalid_credentials(client: TestClient):
    response = client.post("/users/session", data={"username": "wrong@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["message"] == "Incorrect email or password"

def test_logout(client: TestClient):
    client.post("/users/signup", json={"fullname": "Test User", "email": "testlogout@example.com", "password": "password123"})
    login_response = client.post("/users/session", data={"username": "testlogout@example.com", "password": "password123"})
    token = login_response.json()["data"]["access_token"]
    response = client.post("/users/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

def test_logout_invalid_token(client: TestClient):
    response = client.post("/users/logout", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert response.json()["message"] == "Session not found"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app  # FastAPI 애플리케이션 임포트
from tests.conftest import client, authenticated_client

def test_create_board(authenticated_client):
    response = authenticated_client.post("/boards/", json={"name": "Test Board", "public": True})
    assert response.status_code == 201
    assert response.json()["message"] == "Board created successfully"

def test_create_board_missing_fields(authenticated_client):
    response = authenticated_client.post("/boards/", json={"public": True})
    assert response.status_code == 422  # Unprocessable Entity

def test_get_board(authenticated_client):
    response = authenticated_client.get("/boards/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Board retrieved successfully"

def test_get_nonexistent_board(authenticated_client):
    response = authenticated_client.get("/boards/999")
    assert response.status_code == 404
    assert response.json()["message"] == "Board not found"

def test_update_board(authenticated_client):
    response = authenticated_client.put("/boards/1", json={"name": "Updated Board", "public": False})
    assert response.status_code == 200
    assert response.json()["message"] == "Board updated successfully"

def test_update_nonexistent_board(authenticated_client):
    response = authenticated_client.put("/boards/999", json={"name": "Updated Board", "public": False})
    assert response.status_code == 404
    assert response.json()["message"] == "Board not found or permission denied"

def test_delete_board(authenticated_client):
    response = authenticated_client.delete("/boards/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Board deleted successfully"

def test_delete_nonexistent_board(authenticated_client):
    response = authenticated_client.delete("/boards/999")
    assert response.status_code == 404
    assert response.json()["message"] == "Board not found or permission denied"

def test_list_boards(authenticated_client):
    response = authenticated_client.get("/boards/")
    assert response.status_code == 200
    assert response.json()["message"] == "Boards retrieved successfully"

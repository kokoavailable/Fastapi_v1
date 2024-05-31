from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from tests.conftest import client

def test_create_post(client: TestClient):
    response = client.post("/posts/", json={"title": "Test Post", "content": "Test Content", "board_sn": 1})
    assert response.status_code == 201
    assert response.json()["message"] == "Post created successfully"

def test_create_post_missing_fields(client: TestClient):
    response = client.post("/posts/", json={"content": "Test Content", "board_sn": 1})
    assert response.status_code == 422  # Unprocessable Entity

def test_get_post(client: TestClient):
    response = client.get("/posts/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Post retrieved successfully"

def test_get_nonexistent_post(client: TestClient):
    response = client.get("/posts/999")
    assert response.status_code == 404
    assert response.json()["message"] == "Post not found"

def test_update_post(client: TestClient):
    response = client.put("/posts/1", json={"title": "Updated Post", "content": "Updated Content"})
    assert response.status_code == 200
    assert response.json()["message"] == "Post updated successfully"

def test_update_nonexistent_post(client: TestClient):
    response = client.put("/posts/999", json={"title": "Updated Post", "content": "Updated Content"})
    assert response.status_code == 404
    assert response.json()["message"] == "Post not found or permission denied"

def test_delete_post(client: TestClient):
    response = client.delete("/posts/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Post deleted successfully"

def test_delete_nonexistent_post(client: TestClient):
    response = client.delete("/posts/999")
    assert response.status_code == 404
    assert response.json()["message"] == "Post not found or permission denied"

def test_list_posts(client: TestClient):
    response = client.get("/posts/", params={"board_sn": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Posts retrieved successfully"

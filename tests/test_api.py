import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_analyze_url_success():
    response = client.post("/api/v1/analyze", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Mock Title"
    assert data["summary"] == "This is a mock summary."

def test_analyze_url_ssrf():
    response = client.post("/api/v1/analyze", json={"url": "http://localhost:8080"})
    assert response.status_code == 422
    assert "SSRF" in response.json()["detail"]

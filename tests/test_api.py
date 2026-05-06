import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.application.analyze_usecase import AnalyzeUrlUseCase
from src.presentation.routers.analyze import get_analyze_usecase
from src.domain.interfaces import IWebContentExtractor, ILLMAnalyzer
from src.domain.models import CategorizationResult

class MockExtractor(IWebContentExtractor):
    async def extract_text(self, url: str):
        return "Mock Title", "Mock Text Content"

class MockAnalyzer(ILLMAnalyzer):
    async def analyze(self, title: str, text: str) -> CategorizationResult:
        return CategorizationResult(
            title=title,
            summary="This is a mock summary.",
            categories=["MockCategory1", "MockCategory2"]
        )

def override_get_analyze_usecase():
    return AnalyzeUrlUseCase(MockExtractor(), MockAnalyzer())

app.dependency_overrides[get_analyze_usecase] = override_get_analyze_usecase

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

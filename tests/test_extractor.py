import pytest
from src.infrastructure.extractor.html_extractor import BeautifulSoupExtractor
import httpx

@pytest.mark.asyncio
async def test_extractor_success(monkeypatch):
    class MockResponse:
        def __init__(self, text):
            self.text = text
        def raise_for_status(self):
            pass

    async def mock_get(*args, **kwargs):
        html = """
        <html>
            <head>
                <title>Test Title</title>
                <style>body { color: red; }</style>
            </head>
            <body>
                <h1>Hello</h1>
                <p>This is a <b>test</b>.</p>
                <script>console.log("ignore me")</script>
            </body>
        </html>
        """
        return MockResponse(html)

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    extractor = BeautifulSoupExtractor()
    title, text = await extractor.extract_text("https://example.com")
    
    assert title == "Test Title"
    assert "Hello" in text
    assert "This is a" in text
    assert "test" in text
    assert "ignore me" not in text
    assert "body { color: red; }" not in text

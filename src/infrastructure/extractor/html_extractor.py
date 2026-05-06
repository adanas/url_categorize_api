import httpx
from bs4 import BeautifulSoup
from src.domain.interfaces import IWebContentExtractor

class BeautifulSoupExtractor(IWebContentExtractor):
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    async def extract_text(self, url: str) -> tuple[str, str]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Fake User-Agent to avoid simple scraping blocks
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            html_content = response.text

        soup = BeautifulSoup(html_content, "lxml")
        
        # Extract title
        title = soup.title.string if soup.title and soup.title.string else ""
        title = title.strip()

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        # Get text
        text = soup.get_text(separator=" ")
        
        import re
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        text = '\n'.join(line for line in lines if line)
        text = re.sub(r'[ \t]+', ' ', text)

        return title, text

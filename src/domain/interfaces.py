from abc import ABC, abstractmethod
from typing import Tuple
from src.domain.models import CategorizationResult

class IWebContentExtractor(ABC):
    @abstractmethod
    async def extract_text(self, url: str) -> Tuple[str, str]:
        """
        Extracts title and main text content from a given URL.
        Returns:
            Tuple[str, str]: (title, text_content)
        """
        pass

class ILLMAnalyzer(ABC):
    @abstractmethod
    async def analyze(self, title: str, text: str) -> CategorizationResult:
        """
        Analyzes text and title to produce a categorization result.
        Returns:
            CategorizationResult
        """
        pass

from src.domain.interfaces import IWebContentExtractor, ILLMAnalyzer
from src.domain.models import AnalyzeRequestUrl, CategorizationResult

class AnalyzeUrlUseCase:
    def __init__(self, extractor: IWebContentExtractor, analyzer: ILLMAnalyzer):
        self.extractor = extractor
        self.analyzer = analyzer

    async def execute(self, url: str) -> CategorizationResult:
        # Validate SSRF
        validated_url = AnalyzeRequestUrl(url)
        
        # 1. Extract content
        title, text = await self.extractor.extract_text(validated_url.url)
        
        # 2. Truncate text to 4000 chars to avoid LLM context limits
        truncated_text = text[:4000]
        
        # 3. Analyze content
        result = await self.analyzer.analyze(title=title, text=truncated_text)
        
        return result

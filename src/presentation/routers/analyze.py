from fastapi import APIRouter, HTTPException, Depends
from src.presentation.schemas import AnalyzeRequest, AnalyzeResponse
from src.application.analyze_usecase import AnalyzeUrlUseCase
from src.domain.interfaces import IWebContentExtractor, ILLMAnalyzer
from src.domain.models import CategorizationResult

router = APIRouter(prefix="/api/v1", tags=["Analyze"])

from src.infrastructure.extractor.html_extractor import BeautifulSoupExtractor
from src.infrastructure.llm.openai_analyzer import LMStudioOpenAIAnalyzer

def get_analyze_usecase() -> AnalyzeUrlUseCase:
    extractor = BeautifulSoupExtractor()
    analyzer = LMStudioOpenAIAnalyzer()
    return AnalyzeUrlUseCase(extractor, analyzer)

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_url(
    request: AnalyzeRequest, 
    usecase: AnalyzeUrlUseCase = Depends(get_analyze_usecase)
):
    try:
        result = await usecase.execute(str(request.url))
        return AnalyzeResponse(
            title=result.title,
            summary=result.summary,
            categories=result.categories
        )
    except ValueError as e:
        # Validation error (e.g. SSRF)
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Catch extraction/LLM errors
        raise HTTPException(status_code=502, detail="ページの取得またはLLM処理に失敗しました。")

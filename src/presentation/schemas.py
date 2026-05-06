from pydantic import BaseModel, HttpUrl, Field
from typing import List

class AnalyzeRequest(BaseModel):
    url: HttpUrl = Field(..., description="解析対象のURL")

class AnalyzeResponse(BaseModel):
    title: str = Field(..., description="抽出したページタイトル")
    summary: str = Field(..., description="LLMが生成したページの説明文要約")
    categories: List[str] = Field(..., max_length=3, description="LLMが推論したカテゴリリスト（最大3件）")

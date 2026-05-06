import os
import json
from openai import AsyncOpenAI
from src.domain.interfaces import ILLMAnalyzer
from src.domain.models import CategorizationResult

class LMStudioOpenAIAnalyzer(ILLMAnalyzer):
    def __init__(self):
        # Read from environment, default to LM Studio local server
        base_url = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
        api_key = os.getenv("LLM_API_KEY", "lm-studio")
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        self.model = os.getenv("LLM_MODEL", "gemma") # Default to gemma

    async def analyze(self, title: str, text: str) -> CategorizationResult:
        system_prompt = (
            "あなたは優秀なアシスタントです。与えられたウェブページのテキストとタイトルを分析し、"
            "以下のJSON形式で要約とカテゴリを出力してください。\n"
            "{\n"
            '  "summary": "要約（200文字以内）",\n'
            '  "categories": ["カテゴリ1", "カテゴリ2", "カテゴリ3"]\n'
            "}\n"
            "必ず有効なJSONオブジェクトのみを出力してください。"
        )

        user_prompt = f"タイトル: {title}\n本文:\n{text}"

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            # If the specific LLM supports response_format
            # response_format={ "type": "json_object" }
        )

        content = response.choices[0].message.content
        
        # Try to parse the output as JSON
        try:
            # Strip markdown code blocks if the LLM adds them
            clean_content = content.strip()
            if clean_content.startswith("```json"):
                clean_content = clean_content[7:]
            if clean_content.startswith("```"):
                clean_content = clean_content[3:]
            if clean_content.endswith("```"):
                clean_content = clean_content[:-3]
                
            data = json.loads(clean_content.strip())
            
            summary = data.get("summary", "要約の生成に失敗しました。")
            categories = data.get("categories", [])
            # Ensure categories is a list of up to 3 items
            if not isinstance(categories, list):
                categories = []
            categories = categories[:3]

            return CategorizationResult(
                title=title,
                summary=summary,
                categories=categories
            )
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return proper JSON
            return CategorizationResult(
                title=title,
                summary="[LLM解析エラー] 応答が不正な形式でした。",
                categories=["Error"]
            )

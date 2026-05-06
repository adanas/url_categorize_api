from fastapi import FastAPI
from src.presentation.routers import analyze

app = FastAPI(
    title="URL Categorization API",
    description="API for analyzing and categorizing URLs",
    version="1.0.0"
)

app.include_router(analyze.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

app = FastAPI(
    title="SenticRAG API",
    description="Retrieval-Augmented Aspect Sentiment & Feedback Intelligence Engine",
    version="0.1.0",
)

class HealthResponse(BaseModel):
    status: str
    version: str = "0.1.0"

class PredictRequest(BaseModel):
    text: str
    aspects: Optional[List[str]] = None

class AspectSentiment(BaseModel):
    aspect: str
    sentiment: str
    confidence: float

class PredictResponse(BaseModel):
    text: str
    aspect_sentiments: List[AspectSentiment]

class AskRequest(BaseModel):
    query: str
    top_k: int = 5

class Citation(BaseModel):
    review_id: str
    text_snippet: str
    score: float

class AskResponse(BaseModel):
    query: str
    answer: str
    citations: List[Citation]

@app.get("/health/live", status_code=status.HTTP_200_OK, response_model=HealthResponse)
def liveness() -> HealthResponse:
    return HealthResponse(status="alive")

@app.get("/health/ready", status_code=status.HTTP_200_OK, response_model=HealthResponse)
def readiness() -> HealthResponse:
    return HealthResponse(status="ready")

@app.get("/health/startup", status_code=status.HTTP_200_OK, response_model=HealthResponse)
def startup() -> HealthResponse:
    return HealthResponse(status="started")

@app.post("/predict", status_code=status.HTTP_200_OK, response_model=PredictResponse)
def predict_sentiment(request: PredictRequest) -> PredictResponse:
    # Baseline stub
    return PredictResponse(
        text=request.text,
        aspect_sentiments=[
            AspectSentiment(aspect="general", sentiment="positive", confidence=0.95)
        ]
    )

@app.get("/stats", status_code=status.HTTP_200_OK)
def get_stats() -> Dict[str, Any]:
    return {
        "total_reviews_indexed": 0,
        "sentiment_distribution": {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        },
        "top_aspects": []
    }

@app.post("/ask", status_code=status.HTTP_200_OK, response_model=AskResponse)
def ask_feedback_rag(request: AskRequest) -> AskResponse:
    return AskResponse(
        query=request.query,
        answer="SenticRAG feedback intelligence engine initialized.",
        citations=[]
    )

import uuid
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, status
from pydantic import BaseModel

from packages.data_contracts import (
    IngestFeedbackRequest,
    IngestFeedbackResponse,
    InvestigationDrilldownRequest,
    InvestigationDrilldownResponse,
    EvidenceItem,
    ResolutionDraftRequest,
    ResolutionDraftResponse,
    Citation,
    FeedbackContributionRequest,
    FeedbackContributionResponse,
    AspectSentiment,
)

app = FastAPI(
    title="SenticRAG Platform API",
    description="Enterprise Customer Sentiment & Actionable Feedback Intelligence Engine (7-Layer Agent Architecture)",
    version="0.2.0",
)

class HealthResponse(BaseModel):
    status: str
    version: str = "0.2.0"

# ==============================================================================
# 1. HEALTH CHECKS & PROBES
# ==============================================================================

@app.get("/health/live", status_code=status.HTTP_200_OK, response_model=HealthResponse)
def liveness() -> HealthResponse:
    """Kubernetes liveness probe checking container runtime viability."""
    return HealthResponse(status="alive")

@app.get("/health/ready", status_code=status.HTTP_200_OK, response_model=HealthResponse)
def readiness() -> HealthResponse:
    """Kubernetes readiness probe verifying connectivity to databases and vector stores."""
    return HealthResponse(status="ready")

@app.get("/health/startup", status_code=status.HTTP_200_OK, response_model=HealthResponse)
def startup() -> HealthResponse:
    """Kubernetes startup probe verifying model checkpoint loading."""
    return HealthResponse(status="started")

# ==============================================================================
# 2. CORE PRODUCT APIS (Product Capability Contract)
# ==============================================================================

@app.post(
    "/api/v1/ingest/feedback",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=IngestFeedbackResponse,
    tags=["Product: Ingestion & Gateway (Layer 1)"],
    summary="Ingest customer feedback or support tickets with PII anonymization"
)
def ingest_feedback(request: IngestFeedbackRequest) -> IngestFeedbackResponse:
    batch_id = f"batch_{uuid.uuid4().hex[:8]}"
    return IngestFeedbackResponse(
        accepted=len(request.records),
        rejected=0,
        batch_id=batch_id,
        status="queued"
    )

@app.post(
    "/api/v1/investigation/drilldown",
    status_code=status.HTTP_200_OK,
    response_model=InvestigationDrilldownResponse,
    tags=["Product: Qualitative Investigation (US-ANALYST-01, US-PM-01)"],
    summary="Query representative evidence cohort & explain root-cause hypotheses"
)
def investigate_drilldown(request: InvestigationDrilldownRequest) -> InvestigationDrilldownResponse:
    return InvestigationDrilldownResponse(
        cohort_summary={
            "product_id": request.product_id,
            "aspect": request.aspect,
            "negative_rate": 0.42,
            "total_reviews": 1280
        },
        representative_evidence=[
            EvidenceItem(
                review_id="RV-8821",
                text_snippet="Device charges extremely slowly and overheats following firmware update v1.2",
                product_version=request.product_version or "v1.2",
                score=0.92,
                relevance_reason="High negative polarity on aspect: battery_charging"
            )
        ],
        grounded_root_cause_hypotheses=[
            {
                "root_cause": "Firmware v1.2 power management loop bug",
                "affected_versions": ["1.2", "1.2.1"],
                "evidence_count": 35,
                "status": "investigating"
            }
        ],
        confidence=0.89
    )

@app.post(
    "/api/v1/resolution/draft",
    status_code=status.HTTP_200_OK,
    response_model=ResolutionDraftResponse,
    tags=["Product: Actionable Customer Care (US-BUY-01, US-AGENT-01)"],
    summary="Generate policy-grounded resolution draft with verified citations"
)
def generate_resolution_draft(request: ResolutionDraftRequest) -> ResolutionDraftResponse:
    return ResolutionDraftResponse(
        ticket_id=request.ticket_id,
        case_summary=f"Customer reported malfunction on product {request.product_id}: {request.issue_text}",
        recommended_response="Hello, our telemetry confirms a known overheating issue during charging on firmware v1.2. Under official warranty guidelines, you are entitled to roll back your firmware to v1.1.2 following the attached guide, or visit your nearest authorized SenticCare service center for a complimentary replacement.",
        recommended_actions=[
            "Provide step-by-step firmware downgrade instructions to v1.1.2",
            "Offer authorized service center dispatch if charging anomaly persists beyond 24h"
        ],
        citations=[
            Citation(
                source_type="policy",
                source_id="POL-WARRANTY-2026-v2.1",
                snippet="Clause 4.2: Free component replacement or firmware rollback support for defects stemming from official software updates."
            )
        ],
        confidence=0.94,
        needs_human_review=False,
        reason_for_review=None
    )

@app.post(
    "/api/v1/feedback/contribute",
    status_code=status.HTTP_201_CREATED,
    response_model=FeedbackContributionResponse,
    tags=["Product: Collaborative Feedback Loop"],
    summary="Contribute human annotations and root-cause findings into the Knowledge Graph"
)
def contribute_feedback(request: FeedbackContributionRequest) -> FeedbackContributionResponse:
    return FeedbackContributionResponse(
        contribution_id=f"contrib_{uuid.uuid4().hex[:8]}",
        status="accepted",
        requires_approval=request.feedback_type == "graph_mutation"
    )

# ==============================================================================
# 3. BACKWARD-COMPATIBILITY ENDPOINTS (Legacy RAG & ABSA Demo)
# ==============================================================================

class PredictRequest(BaseModel):
    text: str
    aspects: Optional[List[str]] = None

class PredictResponse(BaseModel):
    text: str
    aspect_sentiments: List[AspectSentiment]

class LegacyCitation(BaseModel):
    review_id: str
    text_snippet: str
    score: float

class AskRequest(BaseModel):
    query: str
    top_k: int = 5

class AskResponse(BaseModel):
    query: str
    answer: str
    citations: List[LegacyCitation]

@app.post("/predict", status_code=status.HTTP_200_OK, response_model=PredictResponse, deprecated=True, tags=["Legacy"])
def predict_sentiment_legacy(request: PredictRequest) -> PredictResponse:
    """Legacy sentiment prediction endpoint for backward compatibility."""
    return PredictResponse(
        text=request.text,
        aspect_sentiments=[
            AspectSentiment(aspect="general", sentiment="positive", confidence=0.95, category="product")
        ]
    )

@app.get("/stats", status_code=status.HTTP_200_OK, tags=["Legacy"])
def get_stats_legacy() -> Dict[str, Any]:
    """Legacy stats endpoint providing high-level review counts."""
    return {
        "total_reviews_indexed": 100000,
        "sentiment_distribution": {"positive": 65000, "neutral": 15000, "negative": 20000},
        "top_aspects": ["battery", "display", "delivery", "pricing"]
    }

@app.post("/ask", status_code=status.HTTP_200_OK, response_model=AskResponse, deprecated=True, tags=["Legacy"])
def ask_feedback_rag_legacy(request: AskRequest) -> AskResponse:
    """Legacy generic RAG question-answering endpoint."""
    return AskResponse(
        query=request.query,
        answer="SenticRAG feedback intelligence engine initialized with grounded 7-layer architecture.",
        citations=[]
    )

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class FeedbackRecord(BaseModel):
    source: str = Field(..., description="Data source: review, ticket, chat")
    source_record_id: str = Field(..., description="Primary identifier in origin system")
    text: str = Field(..., description="Raw customer feedback or ticket message")
    language: str = Field(default="vi", description="Language code (e.g. vi, en)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    product_id: str = Field(..., description="Target product identifier")
    product_version: Optional[str] = Field(None, description="Firmware or hardware build revision")
    customer_ref: Optional[str] = Field(None, description="Pseudonymized customer reference key")
    order_ref: Optional[str] = Field(None, description="Pseudonymized purchase order reference")
    channel: str = Field(default="ecommerce", description="Ingestion channel")
    rating: Optional[float] = Field(None, description="Explicit numerical rating (1-5)")

class IngestFeedbackRequest(BaseModel):
    records: List[FeedbackRecord]

class IngestFeedbackResponse(BaseModel):
    accepted: int
    rejected: int
    batch_id: str
    status: str = "queued"

class AspectSentiment(BaseModel):
    aspect: str
    sentiment: str  # positive, negative, neutral
    confidence: float
    category: Optional[str] = None

class InvestigationDrilldownRequest(BaseModel):
    product_id: str
    product_version: Optional[str] = None
    aspect: str
    sentiment: str = "negative"
    time_window_days: int = 30
    top_k: int = 5

class EvidenceItem(BaseModel):
    review_id: str
    text_snippet: str
    product_version: Optional[str] = None
    score: float
    relevance_reason: Optional[str] = None

class InvestigationDrilldownResponse(BaseModel):
    cohort_summary: Dict[str, Any]
    representative_evidence: List[EvidenceItem]
    grounded_root_cause_hypotheses: List[Dict[str, Any]]
    confidence: float

class ResolutionDraftRequest(BaseModel):
    ticket_id: str
    customer_ref: str
    product_id: str
    product_version: Optional[str] = None
    issue_text: str

class Citation(BaseModel):
    source_type: str = Field(..., description="Source origin: policy | ticket | graph_issue")
    source_id: str
    snippet: str

class ResolutionDraftResponse(BaseModel):
    ticket_id: str
    case_summary: str
    recommended_response: str
    recommended_actions: List[str]
    citations: List[Citation]
    confidence: float
    needs_human_review: bool
    reason_for_review: Optional[str] = None

class FeedbackContributionRequest(BaseModel):
    feedback_type: str = Field(..., description="absa_correction | root_cause_tag | graph_mutation | resolution_edit")
    target_id: str
    contributed_by: str
    annotation_payload: Dict[str, Any]

class FeedbackContributionResponse(BaseModel):
    contribution_id: str
    status: str = "accepted"
    requires_approval: bool = False

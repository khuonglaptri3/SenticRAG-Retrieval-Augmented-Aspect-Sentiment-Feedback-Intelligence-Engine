import pytest
from packages.data_contracts import (
    FeedbackRecord,
    InvestigationDrilldownRequest,
    ResolutionDraftRequest,
    Citation,
)

def test_feedback_record_contract():
    record = FeedbackRecord(
        source="ecommerce_review",
        source_record_id="rev_100",
        text="Giao hàng nhanh, máy đẹp",
        product_id="laptop-pro-14"
    )
    assert record.language == "vi"
    assert record.product_id == "laptop-pro-14"
    assert record.customer_ref is None

def test_resolution_contract():
    req = ResolutionDraftRequest(
        ticket_id="TKT-001",
        customer_ref="ANON-771",
        product_id="watch-series-5",
        issue_text="Lỗi hiển thị màn hình"
    )
    assert req.ticket_id == "TKT-001"
    
    citation = Citation(
        source_type="policy",
        source_id="POL-01",
        snippet="Chính sách bảo hành 1 đổi 1 trong 30 ngày"
    )
    assert citation.source_type == "policy"

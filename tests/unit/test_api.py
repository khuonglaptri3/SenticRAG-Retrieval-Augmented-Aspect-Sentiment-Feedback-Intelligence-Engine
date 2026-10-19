from fastapi.testclient import TestClient
from apps.api.app.main import app

client = TestClient(app)

def test_health_live():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"

def test_health_ready():
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_ingest_feedback_api():
    payload = {
        "records": [
            {
                "source": "review",
                "source_record_id": "rv_001",
                "text": "Máy rất nhanh hết pin sau khi update",
                "product_id": "phone-x"
            }
        ]
    }
    response = client.post("/api/v1/ingest/feedback", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert data["accepted"] == 1
    assert data["status"] == "queued"

def test_investigation_drilldown_api():
    payload = {
        "product_id": "phone-x",
        "aspect": "pin",
        "sentiment": "negative",
        "top_k": 3
    }
    response = client.post("/api/v1/investigation/drilldown", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "cohort_summary" in data
    assert len(data["representative_evidence"]) > 0

def test_resolution_draft_api():
    payload = {
        "ticket_id": "tkt_12345",
        "customer_ref": "cust_anon_99",
        "product_id": "phone-x",
        "issue_text": "Pin sạc chậm và nóng máy"
    }
    response = client.post("/api/v1/resolution/draft", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == "tkt_12345"
    assert len(data["citations"]) > 0
    assert "recommended_response" in data

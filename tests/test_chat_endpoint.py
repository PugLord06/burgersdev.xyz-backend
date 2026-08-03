import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tier1_fastapi_startup_and_health():
    """Tier 1: Verify FastAPI application startup and health endpoints."""
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert res_root.json().get("status") == "online"

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json().get("status") == "healthy"

def test_tier1_sse_stream_response_structure():
    """Tier 1: Verify POST /chat SSE stream headers and chunk data formatting."""
    response = client.post("/chat", json={"query": "Tell me about Michael"})
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")
    
    body = response.text
    assert "data: " in body, "Response must contain SSE data headers."

def test_tier2_empty_query_handling():
    """Tier 2: Verify empty query payload returns 400 Bad Request."""
    res_empty_query = client.post("/chat", json={"query": ""})
    assert res_empty_query.status_code == 400

    res_blank = client.post("/chat", json={"message": "   "})
    assert res_blank.status_code == 400

def test_tier2_invalid_payload_format():
    """Tier 2: Verify malformed JSON payload returns 422 Unprocessable Entity."""
    res_invalid_json = client.post(
        "/chat",
        content="not valid json",
        headers={"Content-Type": "application/json"}
    )
    assert res_invalid_json.status_code == 422

    res_wrong_fields = client.post("/chat", json={"foo": "bar"})
    assert res_wrong_fields.status_code == 400

def test_tier2_long_query_handling():
    """Tier 2: Verify handling of large query payload (>2000 characters)."""
    long_query = "What is Michael's background? " + ("detail " * 400)
    assert len(long_query) > 2000
    response = client.post("/chat", json={"query": long_query})
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")
    assert len(response.text) > 0

def test_tier2_message_field_support():
    """Tier 2: Verify POST /chat accepts payload with 'message' field."""
    response = client.post("/chat", json={"message": "What is Michael's degree?"})
    assert response.status_code == 200
    assert "data: " in response.text

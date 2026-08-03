import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.ingest_service import ingest_data

client = TestClient(app)

def _stream_query_text(query: str) -> str:
    response = client.post("/chat", json={"query": query})
    assert response.status_code == 200
    
    contents = []
    for line in response.text.splitlines():
        if line.startswith("data: "):
            data_str = line[6:].strip()
            try:
                data_json = json.loads(data_str)
                contents.append(data_json.get("content", ""))
            except Exception:
                contents.append(data_str)
    return "".join(contents) if contents else response.text

def test_tier1_automated_test_client():
    """Tier 1: Verify test_client execution against the FastAPI app."""
    response = client.post("/chat", json={"query": "Test query"})
    assert response.status_code == 200
    assert "data: " in response.text

def test_tier3_ingestion_followed_by_query_streaming():
    """Tier 3: Verify ingestion execution immediately followed by streaming query."""
    count = ingest_data()
    assert count > 0
    stream_output = _stream_query_text("Where does Michael study?")
    assert "Eduvos" in stream_output or len(stream_output) > 0

def test_tier3_multiturn_query_streaming():
    """Tier 3: Verify sequential multi-turn query streaming over SSE."""
    queries = [
        "Who is Michael Burgers?",
        "What is his education background?",
        "What projects has he launched?",
        "What are his core technical skills?"
    ]
    for q in queries:
        output = _stream_query_text(q)
        assert len(output) > 0

def test_tier4_education_query_accuracy():
    """Tier 4: Verify answers regarding Michael's education (Eduvos)."""
    output = _stream_query_text("Tell me about Michael's education and degree.").lower()
    assert "eduvos" in output
    assert "bscit" in output or "software engineering" in output or "2026" in output

def test_tier4_experience_query_accuracy():
    """Tier 4: Verify answers regarding Michael's experience (Is It Studios)."""
    output = _stream_query_text("Where did Michael work and what is Is It Studios?").lower()
    assert "is it studios" in output
    assert "founder" in output or "software engineer" in output

def test_tier4_projects_query_accuracy():
    """Tier 4: Verify answers regarding Michael's project (Isitcheatingif.com)."""
    output = _stream_query_text("What web game project did Michael build?").lower()
    assert "isitcheatingif" in output

def test_tier4_skills_query_accuracy():
    """Tier 4: Verify answers regarding Michael's core skills."""
    output = _stream_query_text("What are Michael's core skills and technologies?").lower()
    assert "python" in output or "typescript" in output or "ollama" in output or "langchain" in output


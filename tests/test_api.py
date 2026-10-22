"""Integration tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "DocAgent" in data["app"]

def test_demo_page_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "DocAgent" in response.text
    assert "Agent Request Console" in response.text

def test_post_agent_standard_proposal():
    payload = {
        "request": "Create a formal Project Proposal for a Q3 Customer Onboarding Automation system at Acme Corp, including problem statement, proposed solution, timeline, budget, and risk mitigation.",
        "model_provider": "fallback"
    }
    response = client.post("/agent", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "plan" in data
    assert len(data["plan"]["tasks"]) >= 5
    assert "reflection_report" in data
    assert data["reflection_report"]["passed"] is True
    assert "document" in data
    assert data["document"]["download_url"].startswith("/download/")
    
    # Test downloading the generated document
    doc_id = data["document"]["doc_id"]
    download_resp = client.get(f"/download/{doc_id}")
    assert download_resp.status_code == 200
    assert "wordprocessingml" in download_resp.headers["content-type"]
    assert len(download_resp.content) > 1000

def test_post_agent_complex_case():
    payload = {
        "request": "Draft a technical specification and rollout strategy for migrating our legacy monolith to microservices next month, but make sure it handles SOC2 compliance, team capacity constraints, and don't spend more than $50k on cloud infra, even though our CTO wants everything on Kubernetes and our lead architect wants serverless.",
        "model_provider": "fallback"
    }
    response = client.post("/agent", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    # Verify autonomous assumptions were made for conflicting requirements
    assumptions = data["plan"]["assumptions_made"]
    assert len(assumptions) >= 2
    assert any("50,000" in a or "budget" in a.lower() for a in assumptions)
    assert any("kubernetes" in a.lower() or "serverless" in a.lower() for a in assumptions)

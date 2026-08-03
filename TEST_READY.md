# TEST_READY: portfolio-ai-backend

## Overview
This document details the test suite tiers, test counts, and invocation commands for verifying the portfolio-ai-backend project.

## Test Tiers & Case Breakdown

| Tier | Description | Test Count | Target Modules & Scenarios |
|------|-------------|------------|----------------------------|
| **Tier 1** | Feature Coverage | 6 | Basic ingestion execution, ChromaDB creation, FastAPI health checks, SSE stream headers, interface contracts, automated test client. |
| **Tier 2** | Boundary & Corner Cases | 7 | Custom path ingestion, missing file errors, empty query handling, invalid JSON payloads, long queries (>2000 chars), 'message' payload field support, LOC < 150 constraint. |
| **Tier 3** | Cross-Feature Combinations | 2 | Re-ingestion followed immediately by query streaming, multi-turn sequential chat queries. |
| **Tier 4** | Real-World Application Scenarios | 4 | Resume detail verification: Education (Eduvos), Experience (Is It Studios), Projects (Isitcheatingif.com), Core Skills (Python/TypeScript). |
| **Total** | **All Tiers** | **19** | **100% Comprehensive Coverage** |

## Test Invocation Commands

### 1. Pytest Test Runner Script
```powershell
.venv\Scripts\python.exe tests/run_tests.py
```

### 2. Direct Pytest Invocation
```powershell
.venv\Scripts\python.exe -m pytest tests/ -v
```

### 3. Automated SSE Streaming Test Client
Ensure Uvicorn server is running (`.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`), then run:
```powershell
.venv\Scripts\python.exe test_client.py "Tell me about Michael's background."
```

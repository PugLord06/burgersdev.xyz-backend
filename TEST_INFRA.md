# E2E Test Infra: portfolio-ai-backend

## Test Philosophy
- Opaque-box, requirement-driven testing based on `ORIGINAL_REQUEST.md`.
- Methodologies: Category-Partition, Boundary Value Analysis, Pairwise Combinatorial, and Real-World Workloads.

## Feature Inventory
| # | Feature | Source | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---------|--------|:------:|:------:|:------:|:------:|
| F1 | Data Ingestion Script & ChromaDB Vector Store | R1 | 5 | 5 | ✓ | ✓ |
| F2 | FastAPI `/chat` SSE Streaming Endpoint | R2 | 5 | 5 | ✓ | ✓ |
| F3 | Automated End-to-End Test Client Script | R3 | 5 | 5 | ✓ | ✓ |
| F4 | Code Modularity & <150 LOC Per File Constraint | R4 | 5 | 5 | ✓ | ✓ |

## Coverage Goals
- Tier 1 (Feature Coverage): Basic ingestion, server health/chat request, streaming chunks, file structure.
- Tier 2 (Boundary & Corner Cases): Empty query, long query, special characters, missing database, line count limits.
- Tier 3 (Cross-Feature Combinations): Re-ingestion followed by immediate stream queries, concurrent requests, server restarts.
- Tier 4 (Real-World Application Scenarios): Querying resume details (Education, Is It Studios, Isitcheatingif.com, Core Skills) and validating accuracy.

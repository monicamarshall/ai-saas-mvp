# AI SaaS MVP — FastAPI · PostgreSQL · OCR (skeleton)
This is a minimal scaffold for the MVP:
- Ingest PDFs/Excel via URL or upload
- Parse to normalized rows (P&L / Rent Roll)
- Validate and persist to Postgres
- Serve aggregates via FastAPI
- (Optional) OCR fallback with Tesseract
- Ready for Docker/Kubernetes/Argo CD

Quick start:
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  export DATABASE_URL=sqlite:///./mvp.db
  uvicorn app.main:app --reload

Endpoints:
- POST /ingest/url?url=...&doc_type=pnl|rent_roll
- POST /ingest/upload (multipart) with doc_type
- GET /financials/summary

Kubernetes:
- See k8s/ for Deployment/Service and Argo CD Application example.

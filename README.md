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

GitHub setup:

cd C:\data\GitOps\ai-saas-mvp_with_ci

# 1) Initialize repo if needed
git init
git branch -M main

# 2) Add a .gitignore if you haven’t already
# (make sure it ignores venv/, storage/, __pycache__/ etc.)

# 3) Commit (skip CI if secrets not set yet)
git add .
git commit -m "Initial MVP import [skip ci]"

# 4) Point to GitHub and push
git remote add origin https://github.com/monicamarshall/ai-saas-mvp.git
git push -u origin main


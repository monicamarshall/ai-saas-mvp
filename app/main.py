from fastapi import FastAPI
from .routers import ingest, financials
app = FastAPI(title="AI SaaS MVP API")
app.include_router(ingest.router)
app.include_router(financials.router)

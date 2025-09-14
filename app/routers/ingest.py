from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal, Base, engine
from .. import models
from ..services import parse_pdf, validate
import os, requests, datetime
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND","local")
if STORAGE_BACKEND == "s3":
    from ..services.storage_s3 import put_bytes
else:
    from ..services.storage_local import put_bytes
router = APIRouter(prefix="/ingest", tags=["ingest"])
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def run_parse(db: Session, doc: models.Document, pdf_bytes: bytes):
    try:
        rows = parse_pdf.extract_rows(pdf_bytes)
        rows = validate.validate_rows(rows)
        for r in rows:
            g = models.GLLine(document_id=doc.id, property_id=None, period_id=None,
                              account=r["account"], amount=r["amount"], memo=r.get("memo"))
            db.add(g)
        doc.status = "parsed"
        db.commit()
    except Exception as e:
        doc.status = "failed"; doc.message = str(e); db.commit()
@router.post("/url")
def ingest_url(url: str, doc_type: str = "pnl", background: BackgroundTasks = None, db: Session = Depends(get_db)):
    if doc_type not in ("pnl","rent_roll"):
        raise HTTPException(400, detail="doc_type must be 'pnl' or 'rent_roll'")
    r = requests.get(url); r.raise_for_status()
    key = f"raw/{doc_type}/{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.pdf"
    storage_key, checksum = put_bytes(key, r.content)
    doc = models.Document(source_url=url, storage_key=storage_key, checksum=checksum, doc_type=models.DocType(doc_type))
    db.add(doc); db.commit(); db.refresh(doc)
    background.add_task(run_parse, db, doc, r.content)
    return {"document_id": doc.id, "storage_key": storage_key, "job_state": "queued"}
@router.post("/upload")
async def ingest_upload(file: UploadFile = File(...), doc_type: str = "pnl", background: BackgroundTasks = None, db: Session = Depends(get_db)):
    content = await file.read()
    key = f"raw/{doc_type}/{file.filename}"
    storage_key, checksum = put_bytes(key, content)
    doc = models.Document(source_url=None, storage_key=storage_key, checksum=checksum, doc_type=models.DocType(doc_type))
    db.add(doc); db.commit(); db.refresh(doc)
    background.add_task(run_parse, db, doc, content)
    return {"document_id": doc.id, "storage_key": storage_key, "job_state": "queued"}

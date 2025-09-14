from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any, List
class IngestURL(BaseModel):
    url: HttpUrl
    doc_type: str
class IngestUploadResponse(BaseModel):
    document_id: int
    storage_key: str
    job_state: str
class GLLineOut(BaseModel):
    account: str
    amount: float
    memo: Optional[str] = None
class SummaryOut(BaseModel):
    totals: Dict[str, float]
    rows: List[GLLineOut]

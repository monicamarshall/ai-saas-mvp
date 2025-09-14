import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_upload_minimal_pdf():
    content = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    files = {"file": ("test.pdf", content, "application/pdf")}
    r = client.post("/ingest/upload?doc_type=pnl", files=files)
    assert r.status_code == 200
    assert "document_id" in r.json()
    s = client.get("/financials/summary").json()
    assert "totals" in s and isinstance(s["totals"], dict)

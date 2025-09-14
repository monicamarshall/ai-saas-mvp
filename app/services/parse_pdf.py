import io, re
import pdfplumber
def extract_rows(pdf_bytes: bytes):
    rows = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                m = re.match(r"\s*([A-Za-z0-9 &_/-]+)\s+(-?\d+(?:\.\d{1,2})?)\s*$", line)
                if m:
                    rows.append({"account": m.group(1).strip(), "amount": float(m.group(2)), "memo": None})
    return rows

def ocr_pdf_to_text(pdf_bytes: bytes) -> str:
    try:
        import pdfplumber, io
        import pytesseract
        from PIL import Image
    except Exception:
        return ""
    text = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            img = page.to_image(resolution=300).original
            text.append(pytesseract.image_to_string(img))
    return "\n".join(text)

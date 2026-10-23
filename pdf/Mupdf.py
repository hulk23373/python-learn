import pymupdf as fitz  # PyMuPDF

def pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=150)
        images.append(pix.tobytes("png"))
    return images
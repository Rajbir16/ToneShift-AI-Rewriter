from PyPDF2 import PdfReader


def parse_pdf(file) -> str:
    reader = PdfReader(file)
    pages_text = []
    for p in reader.pages:
        pages_text.append(p.extract_text() or "")
    return "\n".join([t for t in pages_text if t.strip()]).strip()


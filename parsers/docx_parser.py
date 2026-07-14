from docx import Document


def parse_docx(file) -> str:
    doc = Document(file)
    parts = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(parts).strip()


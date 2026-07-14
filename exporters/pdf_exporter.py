from io import BytesIO
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_LEFT


def export_pdf(data: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='pre', fontName='Courier', wordWrap='CJK', alignment=TA_LEFT))
    story = []

    ts = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Metadata
    story.append(Paragraph("ToneShift Rewrite", styles['h1']))
    story.append(Paragraph(f"Date: {ts}", styles['Normal']))
    story.append(Paragraph(f"Audience: {data['audience']}", styles['Normal']))
    story.append(Paragraph(f"Tone: {data['tone']}", styles['Normal']))
    story.append(Spacer(1, 24))

    # Original Text
    story.append(Paragraph("Original Text", styles['h2']))
    story.append(Paragraph(data['original_text'].replace('\n', '<br/>'), styles['pre']))
    story.append(Spacer(1, 24))

    # Rewritten Text
    story.append(Paragraph("Rewritten Text", styles['h2']))
    story.append(Paragraph(data['rewritten_text'].replace('\n', '<br/>'), styles['pre']))

    doc.build(story)
    return buffer.getvalue()

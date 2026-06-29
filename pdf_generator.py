from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

REPORT_FOLDER = "reports"

os.makedirs(REPORT_FOLDER, exist_ok=True)


def generate_pdf(content, filename="prescription_report.pdf"):

    pdf_path = os.path.join(REPORT_FOLDER, filename)

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Prescription Report</b>", styles["Title"]))
    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    for line in content.split("\n"):
        story.append(Paragraph(line, styles["BodyText"]))

    doc.build(story)

    return pdf_path
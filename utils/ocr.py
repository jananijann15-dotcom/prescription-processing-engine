import os

try:
    import easyocr
except ImportError:
    easyocr = None

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

reader = None
if easyocr is not None:
    reader = easyocr.Reader(["en"], gpu=False)


def extract_text(image_path):
    """Extract text from a prescription image or PDF."""
    ext = os.path.splitext(image_path)[1].lower()

    if ext == ".pdf":
        if PdfReader is not None:
            pdf = PdfReader(image_path)
            text_chunks = []
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_chunks.append(page_text)
            if text_chunks:
                return "\n\n".join(text_chunks)
        return "PDF text extraction was not available. Please upload a clearer image or install OCR dependencies."

    if reader is not None:
        result = reader.readtext(image_path)
        extracted_text = "\n".join(item[1] for item in result if item[1])
        if extracted_text.strip():
            return extracted_text

    if pytesseract is not None and Image is not None:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)

    return "OCR could not extract text. Please verify your OCR dependencies are installed."

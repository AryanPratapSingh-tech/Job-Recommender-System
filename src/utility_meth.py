import fitz  # PyMuPDF
 
 
def extract_text_from_pdf(pdf_path) -> str:
    """Extract raw text from an uploaded PDF file."""
    doc = fitz.open(stream=pdf_path.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()
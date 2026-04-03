import pdfplumber


def extract_pdf_text(path: str) -> str:
    text_chunks: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_chunks.append(page.extract_text() or '')
    return '
'.join(text_chunks)

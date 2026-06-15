from pypdf import PdfReader


def extract_text_from_pdf(file_path: str):

    reader = PdfReader(file_path)

    full_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            full_text += text

    return full_text

def chunk_text(
    text: str,
    chunk_size: int = 500
):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks
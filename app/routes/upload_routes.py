import os

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

from app.services.pdf_service import (
    extract_text_from_pdf,
    chunk_text
)

from app.services.vector_service import (
    store_chunks
)

router = APIRouter()


@router.post("/upload")

async def upload_pdf(

    conversation_id: str = Form(...),

    file: UploadFile = File(...)
):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:

        content = await file.read()

        buffer.write(content)

    extracted_text = extract_text_from_pdf(
        file_path
    )

    chunks = chunk_text(
        extracted_text
    )

    store_chunks(
        chunks,
        conversation_id
    )

    return {
        "message": "PDF uploaded successfully",
        "conversation_id": conversation_id,
        "chunks_stored": len(chunks)
    }
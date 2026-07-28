import os

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.document_service import (
    save_uploaded_document,
)

from app.services.pdf_service import (
    extract_text_from_pdf,
    chunk_text,
)

from app.services.vector_service import (
    store_chunks,
)

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    conversation_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    os.makedirs(
        "uploads",
        exist_ok=True,
    )

    file_path = f"uploads/{file.filename}"

    content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    extracted_text = extract_text_from_pdf(
        file_path,
    )

    chunks = chunk_text(
        extracted_text,
    )

    store_chunks(
        chunks,
        conversation_id,
    )

    save_uploaded_document(
        db=db,
        conversation_id=conversation_id,
        file_name=file.filename,
        file_size=len(content),
    )

    return {
        "message": "PDF uploaded successfully",
        "conversation_id": conversation_id,
        "file_name": file.filename,
        "file_size": len(content),
        "chunks_stored": len(chunks),
    }
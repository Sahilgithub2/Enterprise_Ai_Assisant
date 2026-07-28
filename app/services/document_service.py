from sqlalchemy.orm import Session

from app.models.uploaded_document import UploadedDocument


def save_uploaded_document(
    db: Session,
    conversation_id: str,
    file_name: str,
    file_size: int,
):
    document = UploadedDocument(
        conversation_id=conversation_id,
        file_name=file_name,
        file_size=file_size,
    )

    db.add(document)
    db.commit()
    
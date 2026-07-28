from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    DateTime,
)

from sqlalchemy.sql import func

from app.core.database import Base


class UploadedDocument(Base):

    __tablename__ = "uploaded_documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id = Column(
        String,
        nullable=False,
        index=True,
    )

    file_name = Column(
        String,
        nullable=False,
    )

    file_size = Column(
        BigInteger,
        nullable=False,
    )

    uploaded_at = Column(
        DateTime,
        server_default=func.now(),
    )
    
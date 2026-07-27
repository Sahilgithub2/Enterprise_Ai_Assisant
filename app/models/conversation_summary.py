from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class ConversationSummary(Base):

    __tablename__ = "conversation_summaries"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    summary = Column(
        Text,
        nullable=False,
        default="",
    )
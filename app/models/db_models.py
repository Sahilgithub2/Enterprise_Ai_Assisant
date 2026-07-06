from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(String, index=True)

    role = Column(String)

    content = Column(Text)

    created_at = Column(String, default="")  # You can use a timestamp or datetime type if needed
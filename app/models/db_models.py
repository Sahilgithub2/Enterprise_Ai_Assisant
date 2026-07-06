from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(
    String,
    index=True,
    nullable=False
)
    

    role = Column(String)

    content = Column(Text)

    created_at = Column(
    DateTime,
    server_default=func.now()
)
    

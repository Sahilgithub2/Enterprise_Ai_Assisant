from sqlalchemy.orm import Session

from app.models.db_models import ChatMessage

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

def get_chat_history(db: Session, session_id: str):

    messages = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id
    ).all()

    history = []

    for msg in messages:

        history.append(
            {
                "role": msg.role,
                "content": msg.content,
                "conversation_id" : msg.conversation_id
            }
        )

    return history


def add_message(
    db: Session,
    conversation_id: str,
    role: str,
    content: str
):

    message = ChatMessage(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)

    db.commit()

def get_langchain_chat_history(
    db: Session,
    conversation_id: str
):

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .all()
    )

    history = []

    for msg in messages:

        if msg.role == "user":

            history.append(
                HumanMessage(content=msg.content)
            )

        else:

            history.append(
                AIMessage(content=msg.content)
            )

    return history
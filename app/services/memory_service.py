from sqlalchemy.orm import Session

from app.models.db_models import ChatMessage


def get_chat_history(db: Session, session_id: str):

    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).all()

    history = []

    for msg in messages:

        history.append(
            {
                "role": msg.role,
                "content": msg.content,
                "session_id" : msg.session_id
            }
        )

    return history


def add_message(
    db: Session,
    session_id: str,
    role: str,
    content: str
):

    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)

    db.commit()
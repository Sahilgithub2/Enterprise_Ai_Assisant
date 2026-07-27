from sqlalchemy.orm import Session

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from app.models.db_models import ChatMessage
from app.models.conversation_summary import ConversationSummary

MAX_HISTORY_MESSAGES = 10


def get_chat_history(
    db: Session,
    conversation_id: str,
):
    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.conversation_id == conversation_id
        )
        .order_by(ChatMessage.created_at.asc())
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


def get_recent_chat_history(
    db: Session,
    conversation_id: str,
    limit: int = MAX_HISTORY_MESSAGES,
):
    history = get_chat_history(
        db,
        conversation_id,
    )

    return history[-limit:]


def add_message(
    db: Session,
    conversation_id: str,
    role: str,
    content: str,
):
    message = ChatMessage(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()


def get_summary(
    db: Session,
    conversation_id: str,
):
    summary = (
        db.query(ConversationSummary)
        .filter(
            ConversationSummary.conversation_id == conversation_id
        )
        .first()
    )

    if summary:
        return summary.summary

    return ""


def save_summary(
    db: Session,
    conversation_id: str,
    summary_text: str,
):
    summary = (
        db.query(ConversationSummary)
        .filter(
            ConversationSummary.conversation_id == conversation_id
        )
        .first()
    )

    if summary:

        summary.summary = summary_text

    else:

        summary = ConversationSummary(
            conversation_id=conversation_id,
            summary=summary_text,
        )

        db.add(summary)

    db.commit()


def get_conversation_text(
    db: Session,
    conversation_id: str,
):
    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.conversation_id == conversation_id
        )
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    conversation = []

    for msg in messages:

        conversation.append(
            f"{msg.role.upper()}: {msg.content}"
        )

    return "\n".join(conversation)


def get_conversation_length(
    db: Session,
    conversation_id: str,
):
    return (
        db.query(ChatMessage)
        .filter(
            ChatMessage.conversation_id == conversation_id
        )
        .count()
    )


def should_summarize(
    db: Session,
    conversation_id: str,
    threshold: int = 20,
):
    return (
        get_conversation_length(
            db,
            conversation_id,
        )
        >= threshold
    )
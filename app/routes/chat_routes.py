from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.models.chat_models import ChatRequest

from app.services.ai_service import ask_ai

from app.services.memory_service import (
    get_chat_history,
    add_message
)

from app.core.database import get_db


router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    add_message(
        db,
        request.conversation_id,
        "user",
        request.question
    )

    history = get_chat_history(
        db,
        request.conversation_id
    )

    ai_response = ask_ai(history)

    add_message(
        db,
        request.conversation_id,
        "assistant",
        ai_response
    )

    return {
        "session_id": request.conversation_id,
        "response": ai_response
    }
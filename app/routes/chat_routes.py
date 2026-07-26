from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.models.chat_models import ChatRequest

from app.services.ai_service import ask_ai

from app.services.memory_service import (
    get_recent_chat_history,
    add_message,
    should_summarize,
)

from app.core.database import get_db


router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    add_message(
        db,
        request.conversation_id,
        "user",
        request.question,
    )

    history = get_recent_chat_history(
        db,
        request.conversation_id,
    )

    if should_summarize(
        db,
        request.conversation_id,
    ):
        print("\n========== MEMORY ==========")
        print("Conversation summary will be generated in a future sprint.")

    ai_response = ask_ai(
        history,
        request.conversation_id,
    )

    add_message(
        db,
        request.conversation_id,
        "assistant",
        ai_response,
    )

    return {
        "session_id": request.conversation_id,
        "response": ai_response,
    }
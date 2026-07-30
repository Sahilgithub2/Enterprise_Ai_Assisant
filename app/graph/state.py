from typing import TypedDict

from sqlalchemy.orm import Session


class GraphState(TypedDict):
    db: Session

    conversation_id: str

    messages: list

    latest_question: str

    chat_history: list

    standalone_question: str

    tools: list[str]

    contexts: list[str]

    accumulated_context: str

    sources: list[str]

    final_answer: str
from app.services.ai_service import (
    generate_summary,
)


def memory_node(state):

    generate_summary(
        state["db"],
        state["conversation_id"],
    )

    return state
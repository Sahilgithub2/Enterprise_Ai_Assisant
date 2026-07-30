from app.services.ai_service import rewrite_question


def rewrite_node(state):

    latest_question = state["messages"][-1].content
    chat_history = state["messages"][:-1]

    standalone_question = rewrite_question(
        chat_history,
        latest_question,
    )

    print("\n========== QUESTION ==========")
    print(f"Original     : {latest_question}")
    print(f"Standalone   : {standalone_question}")

    state["latest_question"] = latest_question
    state["chat_history"] = chat_history
    state["standalone_question"] = standalone_question

    return state
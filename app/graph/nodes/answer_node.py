from app.services.ai_service import (
    llm,
)

from app.prompts.chat_prompts import (
    answer_prompt,
)


def answer_node(state):

    contexts = state["contexts"]

    context = "\n\n".join(state["contexts"])

    prompt = answer_prompt.invoke(
        {
            "chat_history": state["chat_history"],
            "context": context,
            "question": state["latest_question"],
        }
    )

    response = llm.invoke(
        prompt
    )

    final_answer = response.content.strip()

    if state["sources"]:

        final_answer += "\n\nSources\n"

        for source in sorted(
            set(state["sources"])
        ):
            final_answer += f"- {source}\n"

    state["final_answer"] = final_answer

    return state
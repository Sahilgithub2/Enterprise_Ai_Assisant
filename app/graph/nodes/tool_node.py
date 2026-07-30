from app.tools import (
    get_pdf_context,
    get_web_context,
    get_sql_context,
    get_jira_context,
)

from app.services.memory_service import (
    get_summary,
)


def tool_node(state):

    db = state["db"]
    conversation_id = state["conversation_id"]

    contexts = []
    sources = []
    accumulated_context = ""

    summary = get_summary(
        db,
        conversation_id,
    )

    if summary:

        summary_context = f"""
Conversation Summary

{summary}
""".strip()

        contexts.append(summary_context)

        accumulated_context += summary_context + "\n\n"

    tool_registry = {
        "PDF": lambda: get_pdf_context(
            state["standalone_question"],
            conversation_id,
            previous_context=accumulated_context,
        ),
        "WEB": lambda: get_web_context(
            state["standalone_question"],
            previous_context=accumulated_context,
        ),
        "SQL": lambda: get_sql_context(
            db,
            state["standalone_question"],
            previous_context=accumulated_context,
        ),
        "JIRA": lambda: get_jira_context(
            state["standalone_question"],
            previous_context=accumulated_context,
        ),
    }

    for tool in state["tools"]:

        if tool not in tool_registry:
            continue

        result = tool_registry[tool]()

        if not result["context"].strip():
            continue

        tool_context = f"""
{tool} Context

{result['context']}
""".strip()

        contexts.append(tool_context)

        accumulated_context += tool_context + "\n\n"

        sources.append(
            result["source"]
        )

    state["contexts"] = contexts
    state["sources"] = sources
    state["accumulated_context"] = accumulated_context

    return state
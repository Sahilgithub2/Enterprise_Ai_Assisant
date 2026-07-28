from sqlalchemy.orm import Session

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

from app.prompts.chat_prompts import (
    rewrite_prompt,
    answer_prompt,
    summary_prompt,
)

from app.prompts.router_prompt import (
    router_prompt,
)

from app.tools import (
    get_pdf_context,
    get_web_context,
    get_sql_context,
    get_jira_context,
)

from app.services.memory_service import (
    get_summary,
    save_summary,
    should_summarize,
    get_conversation_text,
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)


def rewrite_question(
    chat_history,
    latest_question,
):
    rewrite_messages = rewrite_prompt.invoke(
        {
            "chat_history": chat_history,
            "question": latest_question,
        }
    )

    response = llm.invoke(rewrite_messages)

    return response.content.strip()


def route_question(
    question,
):
    router_messages = router_prompt.invoke(
        {
            "question": question,
        }
    )

    response = llm.invoke(router_messages)

    return [
        tool.strip().upper()
        for tool in response.content.split(",")
        if tool.strip()
    ]


def generate_summary(
    db: Session,
    conversation_id: str,
):
    if not should_summarize(
        db,
        conversation_id,
    ):
        return

    conversation = get_conversation_text(
        db,
        conversation_id,
    )

    prompt = summary_prompt.invoke(
        {
            "conversation": conversation,
        }
    )

    response = llm.invoke(prompt)

    save_summary(
        db,
        conversation_id,
        response.content.strip(),
    )

    print("\n========== MEMORY SUMMARY UPDATED ==========")


def ask_ai(
    db: Session,
    messages,
    conversation_id,
):
    latest_question = messages[-1].content
    chat_history = messages[:-1]

    standalone_question = rewrite_question(
        chat_history,
        latest_question,
    )

    print("\n========== QUESTION ==========")
    print(f"Original     : {latest_question}")
    print(f"Standalone   : {standalone_question}")

    tools = route_question(
        standalone_question,
    )

    print("\n========== ROUTER ==========")
    print(tools)

    contexts = []
    sources = []

    summary = get_summary(
        db,
        conversation_id,
    )

    if summary:

        contexts.append(
            f"""
Conversation Summary

{summary}
"""
        )

    if "PDF" in tools:

        pdf_result = get_pdf_context(
            standalone_question,
            conversation_id,
        )

        if pdf_result["context"].strip():

            contexts.append(
                f"""
PDF Context

{pdf_result['context']}
"""
            )

            sources.append(
                pdf_result["source"]
            )

    if "WEB" in tools:

        web_result = get_web_context(
            standalone_question,
        )

        if web_result["context"].strip():

            contexts.append(
                f"""
Web Context

{web_result['context']}
"""
            )

            sources.append(
                web_result["source"]
            )

    if "SQL" in tools:

        sql_result = get_sql_context(
            db,
            standalone_question,
        )

        if sql_result["context"].strip():

            contexts.append(
                f"""
SQL Context

{sql_result['context']}
"""
            )

            sources.append(
                sql_result["source"]
            )

        if "JIRA" in tools:

                jira_result = get_jira_context(
                    standalone_question,
                )

                if jira_result["context"].strip():

                    contexts.append(
                        f"""
        Jira Context

        {jira_result['context']}
        """
                    )

                    sources.append(
                        jira_result["source"]
                    )
        
    if not contexts:

        contexts.append(
            "No relevant context available."
        )

    prompt = answer_prompt.invoke(
        {
            "chat_history": chat_history,
            "context": "\n\n".join(contexts),
            "question": latest_question,
        }
    )

    response = llm.invoke(
        prompt
    )

    generate_summary(
        db,
        conversation_id,
    )

    final_answer = response.content.strip()

    if sources:

        final_answer += "\n\nSources\n"

        for source in sorted(set(sources)):
            final_answer += f"- {source}\n"

    return final_answer

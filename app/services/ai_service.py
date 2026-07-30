from sqlalchemy.orm import Session

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI
import os
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


llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_API_BASE"],
    api_key=os.environ["AZURE_API_KEY"],
    api_version=os.environ["AZURE_API_VERSION"],
    azure_deployment="gpt-5"
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

    if "PDF" in tools:

        pdf_result = get_pdf_context(
            standalone_question,
            conversation_id,
            previous_context=accumulated_context,
        )

        if pdf_result["context"].strip():

            pdf_context = f"""
PDF Context

{pdf_result['context']}
""".strip()

            contexts.append(pdf_context)

            accumulated_context += pdf_context + "\n\n"

            sources.append(
                pdf_result["source"]
            )

    if "WEB" in tools:

        web_result = get_web_context(
            standalone_question,
            previous_context=accumulated_context,
        )

        if web_result["context"].strip():

            web_context = f"""
Web Context

{web_result['context']}
""".strip()

            contexts.append(web_context)

            accumulated_context += web_context + "\n\n"

            sources.append(
                web_result["source"]
            )

    if "SQL" in tools:

        sql_result = get_sql_context(
            db,
            standalone_question,
            previous_context=accumulated_context,
        )

        if sql_result["context"].strip():

            sql_context = f"""
SQL Context

{sql_result['context']}
""".strip()

            contexts.append(sql_context)

            accumulated_context += sql_context + "\n\n"

            sources.append(
                sql_result["source"]
            )

    if "JIRA" in tools:

        jira_result = get_jira_context(
            standalone_question,
            previous_context=accumulated_context,
        )

        if jira_result["context"].strip():

            jira_context = f"""
Jira Context

{jira_result['context']}
""".strip()

            contexts.append(jira_context)

            accumulated_context += jira_context + "\n\n"

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
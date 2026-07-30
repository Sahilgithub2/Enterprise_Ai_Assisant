from sqlalchemy.orm import Session

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI
import os

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

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

from app.prompts.chat_prompts import (
    rewrite_prompt,
    answer_prompt,
)

from app.prompts.router_prompt import (
    router_prompt,
)

from app.tools import (
    get_pdf_context,
    get_web_context,
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

    tools = [
        tool.strip().upper()
        for tool in response.content.split(",")
        if tool.strip()
    ]

    return tools


def ask_ai(
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

    if not contexts:

        contexts.append(
            "No relevant context was retrieved."
        )

    combined_context = "\n\n".join(
        contexts
    )

    formatted_prompt = answer_prompt.invoke(
        {
            "chat_history": chat_history,
            "context": combined_context,
            "question": latest_question,
        }
    )

    response = llm.invoke(
        formatted_prompt
    )

    final_answer = response.content.strip()

    if sources:

        unique_sources = list(
            dict.fromkeys(sources)
        )

        final_answer += "\n\nSources\n"

        for source in unique_sources:
            final_answer += f"- {source}\n"

    return final_answer

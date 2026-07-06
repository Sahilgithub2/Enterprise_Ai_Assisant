from urllib import response

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

from app.services.vector_service import (
    search_chunks
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)


def ask_ai(messages):

    latest_question = messages[-1]["content"]

    conversation_id = messages[0].get(
    "conversation_id"
)

    retrieved_chunks = search_chunks(
        latest_question,
        conversation_id
)

    context = "\n".join(retrieved_chunks)

    conversation_history = ""

    for message in messages:

        conversation_history += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    formatted_prompt = f"""
    You are a helpful AI assistant.

    Use the conversation history for memory/context.

    Use the retrieved document context when answering
    document-related questions.

    -------------------------
    Conversation History:
    {conversation_history}

    -------------------------
    Retrieved Document Context:
    {context}

    -------------------------
    Latest User Question:
    {latest_question}
    """

    response = llm.invoke(
    formatted_prompt
)

    return response.content


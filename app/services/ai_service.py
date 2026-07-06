
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

from app.services.vector_service import (
    search_chunks
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Use the retrieved document context when answering document-related questions.

If the answer is not present in the document, answer using your general knowledge and clearly indicate that it was not found in the uploaded document.
"""
        ),

        (
            "human",
            """
Conversation History:

{history}

---------------------

Retrieved Context:

{context}

---------------------

Question:

{question}
"""
        )
    ]
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

    for message in messages[:-1]:

        conversation_history += (
        f"{message['role'].capitalize()}: "
        f"{message['content']}\n"
)

    formatted_prompt = prompt.invoke(
    {
        "history": conversation_history,
        "context": context,
        "question": latest_question
    }
)
    response = llm.invoke(
    formatted_prompt
)

    return response.content


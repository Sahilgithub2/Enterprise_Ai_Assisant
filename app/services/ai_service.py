
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

from app.services.vector_service import (
    search_chunks
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Use the retrieved document context when answering
document-related questions.

If the answer is not present in the document,
answer using your general knowledge and clearly
indicate that it was not found in the uploaded document.
"""
        ),

        MessagesPlaceholder(
            variable_name="chat_history"
        ),

        (
            "human",
            """
Retrieved Document Context:

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


def ask_ai(
    messages,
    conversation_id
):

    latest_question = messages[-1].content

    chat_history = messages[:-1]

    retrieved_chunks = search_chunks(
        latest_question,
        conversation_id
    )

    context = "\n".join(
        retrieved_chunks
    )

    formatted_prompt = prompt.invoke(
        {
            "chat_history": chat_history,
            "context": context,
            "question": latest_question
        }
    )

    response = llm.invoke(
        formatted_prompt
    )

    return response.content

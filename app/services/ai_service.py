from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from app.core.config import GEMINI_API_KEY

from app.services.vector_service import (
    vector_store,
    rerank_chunks,
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)


rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Given the chat history and the latest user question,
rewrite the latest user question into a standalone question
that can be understood without the previous conversation.

Do NOT answer the question.

Only rewrite it if necessary.
Otherwise return it unchanged.
"""
        ),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        (
            "human",
            "{question}"
        ),
    ]
)


answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Use the retrieved document context when answering document-related questions.

If the answer is not present in the document, answer using your general knowledge and clearly indicate that it was not found in the uploaded document.
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
        ),
    ]
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

    response = llm.invoke(
        rewrite_messages
    )

    return response.content.strip()


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

    print(f"Original Question: {latest_question}")
    print(f"Standalone Question: {standalone_question}")

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 10,
            "filter": {
                "conversation_id": conversation_id,
            },
        }
    )

    documents = retriever.invoke(
        standalone_question
    )

    chunks = [
        document.page_content
        for document in documents
    ]

    retrieved_chunks = rerank_chunks(
        standalone_question,
        chunks,
    )

    context = "\n".join(retrieved_chunks)

    formatted_prompt = answer_prompt.invoke(
        {
            "chat_history": chat_history,
            "context": context,
            "question": latest_question,
        }
    )

    response = llm.invoke(
        formatted_prompt
    )

    return response.content


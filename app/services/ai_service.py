from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

from app.prompts.chat_prompts import (
    rewrite_prompt,
    answer_prompt,
)

from app.prompts.web_prompts import (
    web_search_prompt,
)

from app.services.vector_service import (
    vector_store,
    rerank_documents,
)

from app.services.web_search_service import (
    search_web,
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)

RETRIEVAL_THRESHOLD = 0.35


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

    print(f"\nOriginal Question: {latest_question}")
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

    retrieved_documents = rerank_documents(
        standalone_question,
        documents,
    )

    print("\nCrossEncoder Scores\n")

    for document, score in retrieved_documents:
        print(f"{score:.4f}")

    best_score = (
        retrieved_documents[0][1]
        if retrieved_documents
        else 0
    )

    print(f"\nBest Score: {best_score:.4f}")

    if best_score >= RETRIEVAL_THRESHOLD:

        print("\nUsing PDF Context\n")

        context = "\n\n".join(
            document.page_content
            for document, score in retrieved_documents
        )

        formatted_prompt = answer_prompt.invoke(
            {
                "chat_history": chat_history,
                "context": context,
                "question": latest_question,
            }
        )

    else:

        print("\nUsing Web Search\n")

        web_context = search_web(
            standalone_question
        )

        formatted_prompt = web_search_prompt.invoke(
            {
                "web_context": web_context,
                "question": latest_question,
            }
        )

    response = llm.invoke(
        formatted_prompt
    )

    return response.content

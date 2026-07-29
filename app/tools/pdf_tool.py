from app.services.vector_service import (
    vector_store,
    rerank_documents,
)


def get_pdf_context(
    question: str,
    conversation_id: str,
    top_k: int = 10,
    previous_context: str = "",
):
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": top_k,
            "filter": {
                "conversation_id": conversation_id,
            },
        }
    )

    documents = retriever.invoke(question)

    if not documents:
        return {
            "context": "",
            "score": float("-inf"),
            "documents": [],
            "source": "Uploaded PDF",
        }

    ranked_documents = rerank_documents(
        question,
        documents,
    )

    print("\n========== PDF Retrieval ==========\n")

    for index, (document, score) in enumerate(ranked_documents, start=1):
        print(f"{index}. Score : {score:.4f}")

    best_score = ranked_documents[0][1]

    context = "\n\n".join(
        document.page_content
        for document, score in ranked_documents
    )

    return {
        "context": context,
        "score": best_score,
        "documents": ranked_documents,
        "source": "Uploaded PDF",
    }

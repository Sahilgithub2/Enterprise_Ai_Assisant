from sentence_transformers import CrossEncoder

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma


embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_store = Chroma(
    collection_name="pdf_documents",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def store_chunks(
    chunks,
    conversation_id
):
    documents = []
    ids = []

    for index, chunk in enumerate(chunks):
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "conversation_id": conversation_id
                }
            )
        )

        ids.append(
            f"{conversation_id}_{index}"
        )

    vector_store.add_documents(
        documents=documents,
        ids=ids
    )


def rerank_documents(
    query,
    documents
):
    if not documents:
        return []

    pairs = [
        [query, document.page_content]
        for document in documents
    ]

    scores = reranker.predict(
        pairs
    )

    scored_documents = list(
        zip(documents, scores)
    )

    scored_documents.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scored_documents[:3]
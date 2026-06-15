import chromadb

from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder


client = chromadb.Client()

collection = client.create_collection(
    name="pdf_documents"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def store_chunks(
    chunks,
    session_id
):

    for index, chunk in enumerate(chunks):

        embedding = embedding_model.encode(chunk)

        collection.add(
            ids=[f"{session_id}_{index}"],

            embeddings=[
                embedding.tolist()
            ],

            documents=[chunk],

            metadatas=[
                {
                    "session_id": session_id
                }
            ]
        )

def search_chunks(
    query: str,
    session_id: str
):

    query_embedding = embedding_model.encode(
        query
    )

    results = collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=10,

        where={
            "session_id": session_id
        }
    )

    retrieved_chunks = results["documents"][0]

    reranked_chunks = rerank_chunks(
    query,
    retrieved_chunks
    )

    return reranked_chunks

def rerank_chunks(
    query,
    chunks
):

    pairs = []

    for chunk in chunks:

        pairs.append(
            [query, chunk]
        )

    scores = reranker.predict(pairs)

    scored_chunks = list(
        zip(chunks, scores)
    )

    scored_chunks.sort(
        key=lambda x: x[1],
        reverse=True
    )

    reranked_chunks = []

    for chunk, score in scored_chunks:

        reranked_chunks.append(chunk)

    return reranked_chunks[:3]
from langchain_core.documents import Document

from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

docs = [

    Document(
        page_content=
        "Redis is an in-memory database used for caching."
    ),

    Document(
        page_content=
        "PostgreSQL is a relational database."
    ),

    Document(
        page_content=
        "ChromaDB is a vector database used in RAG systems."
    )
]

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model
)

retriever = vectorstore.as_retriever()

results = retriever.invoke(
    "Tell me about Redis"
)

for doc in results:

    print(doc.page_content)


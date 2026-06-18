from langchain_core.documents import Document

docs = [
    Document(
        page_content="Redis is an in-memory database."
    ),
    Document(
        page_content="PostgreSQL is a relational database."
    ),
    Document(
        page_content="ChromaDB is a vector database."
    )
]

for doc in docs:
    print(doc)
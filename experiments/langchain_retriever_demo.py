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

query = "Tell me about Redis"

for doc in docs:

    if "Redis" in doc.page_content:

        print(doc.page_content)
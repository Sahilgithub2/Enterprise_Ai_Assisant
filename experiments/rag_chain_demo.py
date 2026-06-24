from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

from langchain_core.documents import Document

from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

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

question = "What is Redis?"

retrieved_docs = retriever.invoke(
    question
)

context = "\n".join(
    [
        doc.page_content
        for doc in retrieved_docs
    ]
)

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful AI assistant.

    Answer using only the provided context.

    Context:
    {context}

    Question:
    {question}
    """
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)

parser = StrOutputParser()

chain = prompt | llm | parser

response = chain.invoke(
    {
        "context": context,
        "question": question
    }
)

print(response)
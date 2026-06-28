from dotenv import load_dotenv

from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

from langchain_core.documents import Document

from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough
)


docs = [

    Document(
        page_content="Redis is an in-memory database used for caching."
    ),

    Document(
        page_content="PostgreSQL is a relational database."
    ),

    Document(
        page_content="ChromaDB is a vector database."
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

def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

prompt = ChatPromptTemplate.from_template(
    """
    You are an AI assistant.

    Answer ONLY using the context below.

    Context:
    {context}

    Question:
    {question}
    """
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

parser = StrOutputParser()

rag_chain = (
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | parser
)

response = rag_chain.invoke(
    "Tell me about Redis."
)

print(response)


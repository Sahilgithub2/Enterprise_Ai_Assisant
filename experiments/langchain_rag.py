from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

prompt = ChatPromptTemplate.from_template(
    """
    You are an AI tutor.

    Answer the question using the context.

    Context:
    {context}

    Question:
    {question}
    """
)

parser = StrOutputParser()

chain = prompt | llm | parser

response = chain.invoke(
    {
        "context":
        "Redis is an in-memory key value database used for caching.",

        "question":
        "What is Redis?"
    }
)

print(response)
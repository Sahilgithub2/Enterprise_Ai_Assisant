from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import (
    StrOutputParser
)

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

prompt = PromptTemplate.from_template(
    """
    Explain:

    {topic}
    """
)

parser = StrOutputParser()

chain = prompt | llm | parser

response = chain.invoke(
    {
        "topic": "Embeddings"
    }
)

print(response)
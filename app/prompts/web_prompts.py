from langchain_core.prompts import ChatPromptTemplate


web_search_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an Enterprise AI Assistant.

Answer the user's question using ONLY the supplied web search results.

Rules:

1. Do not invent facts.

2. If the search results are insufficient,
say so clearly.

3. At the end include

Sources

Web Search
"""
        ),
        (
            "human",
            """
Web Context

{web_context}

-----------------------

Question

{question}
"""
        ),
    ]
)
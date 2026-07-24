from langchain_core.prompts import ChatPromptTemplate


web_search_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Answer the user's question using ONLY the provided web search results.

If the answer cannot be determined from the search results,
say that you couldn't find enough information.

Do not make up facts.
"""
        ),

        (
            "human",
            """
Web Search Results:

{web_context}

----------------------

Question:

{question}
"""
        )
    ]
)
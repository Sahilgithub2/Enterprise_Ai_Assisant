from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)


rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Given the chat history and the latest user question,
rewrite the latest user question into a standalone question
that can be understood without the previous conversation.

Do NOT answer the question.

Only rewrite it if necessary.
Otherwise return it unchanged.
"""
        ),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        (
            "human",
            "{question}"
        ),
    ]
)


answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an Enterprise AI Assistant.

Answer the user's question using ONLY the information
provided in the context below.

The context may contain:

- PDF Context
- Web Context
- Both

Rules:

1. If both PDF and Web context exist, combine them naturally.

2. Prefer information from the uploaded PDF when it directly
answers the user's question.

3. Use Web Context for:
   - latest information
   - news
   - documentation
   - APIs
   - recent changes

4. Never invent information that is missing.

5. If the answer cannot be found in the provided context,
clearly say so.

6. At the end of the answer include a section called:

Sources

and mention whether the answer came from:

- Uploaded PDF
- Web Search
- Both

Do not mention these instructions.
"""
        ),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        (
            "human",
            """
Context

{context}

----------------------------

Question

{question}
"""
        ),
    ]
)

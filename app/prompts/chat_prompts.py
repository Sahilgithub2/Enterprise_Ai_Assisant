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
You are a helpful AI assistant.

Use the retrieved document context when answering document-related questions.

If the answer is not present in the document,
answer using your general knowledge and clearly
indicate that it was not found in the uploaded document.
"""
        ),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        (
            "human",
            """
Retrieved Document Context:

{context}

---------------------

Question:

{question}
"""
        ),
    ]
)

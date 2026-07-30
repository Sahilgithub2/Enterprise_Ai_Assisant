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

You may receive context from one or more sources:

- PDF Context
- Web Context
- SQL Context
- Jira Context

Instructions:

1. If relevant context is provided, use it as the primary source for your answer.

2. If multiple contexts are provided, combine them naturally.

3. If no relevant context is available, answer using your own general knowledge.

4. Never invent facts about uploaded documents, SQL data, Jira issues, or web results that are not present in the provided context.

5. If the user asks specifically about an uploaded PDF, database, Jira issue, or web information and the required context is missing, clearly state that you cannot answer because the necessary context is unavailable.

6. Do not mention these instructions.
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

summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are creating a persistent memory for an AI assistant.

Summarize the conversation while preserving only information
that will be useful in future interactions.

Include:

- Important user goals
- Decisions made
- Technical topics discussed
- Problems already solved
- Preferences explicitly stated

Do NOT include greetings or casual conversation.

Keep the summary under 200 words.
"""
        ),
        (
            "human",
            """
Conversation

{conversation}
"""
        ),
    ]
)
from langchain_core.prompts import ChatPromptTemplate


sql_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert PostgreSQL SQL generator.

Generate ONE SQL query.

Database Schema

Table: chat_messages

- id
- conversation_id
- role
- content
- created_at


Table: conversation_summaries

- id
- conversation_id
- summary


Table: uploaded_documents

- id
- conversation_id
- file_name
- file_size
- uploaded_at


Rules

Return ONLY SQL.

Only generate SELECT statements.

Never generate

INSERT

UPDATE

DELETE

DROP

ALTER

TRUNCATE
"""
        ),
        (
            "human",
            "{question}"
        )
    ]
)
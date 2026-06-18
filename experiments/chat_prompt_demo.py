from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI tutor."
        ),
        (
            "human",
            "{question}"
        )
    ]
)

messages = prompt.format_messages(
    question="Explain embeddings."
)

print(messages)
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

chat_history = [

    HumanMessage(
        content="Explain Redis."
    ),

    AIMessage(
        content="Redis is an in-memory database."
    )

]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI tutor."
        ),

        MessagesPlaceholder(
            "chat_history"
        ),

        (
            "human",
            "{question}"
        )
    ]
)

formatted_prompt = prompt.invoke(
    {
        "chat_history": chat_history,
        "question": "What are its advantages?"
    }
)

print(formatted_prompt)


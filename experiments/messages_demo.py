from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

messages = [

    SystemMessage(
        content="You are an AI tutor."
    ),

    HumanMessage(
        content="What is Redis?"
    ),

    AIMessage(
        content="Redis is an in-memory database."
    )
]

for message in messages:

    print(type(message))

    print(message.content)

    print("-"*40)


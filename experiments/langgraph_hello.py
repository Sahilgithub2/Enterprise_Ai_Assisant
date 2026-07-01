from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

class ChatState(TypedDict):

    message: str

def greeting_node(state: ChatState):

    print("Current State:")

    print(state)

    return state


graph_builder = StateGraph(ChatState)
graph_builder.add_node(
    "greeting",
    greeting_node
)

graph_builder.add_edge(
    START,
    "greeting"
)
graph_builder.add_edge(
    "greeting",
    END
)

graph = graph_builder.compile()

result = graph.invoke(
    {
        "message":
        "Hello LangGraph!"
    }
)

print(result)

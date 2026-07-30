from langgraph.graph import (
    START,
    END,
    StateGraph,
)

from app.graph.state import GraphState

from app.graph.nodes.rewrite_node import (
    rewrite_node,
)

from app.graph.nodes.router_node import (
    router_node,
)

from app.graph.nodes.tool_node import (
    tool_node,
)

from app.graph.nodes.answer_node import (
    answer_node,
)

from app.graph.nodes.memory_node import (
    memory_node,
)


builder = StateGraph(
    GraphState
)

builder.add_node(
    "rewrite",
    rewrite_node,
)

builder.add_node(
    "router",
    router_node,
)

builder.add_node(
    "tools",
    tool_node,
)

builder.add_node(
    "answer",
    answer_node,
)

builder.add_node(
    "memory",
    memory_node,
)

builder.add_edge(
    START,
    "rewrite",
)

builder.add_edge(
    "rewrite",
    "router",
)

builder.add_edge(
    "router",
    "tools",
)

builder.add_edge(
    "tools",
    "answer",
)

builder.add_edge(
    "answer",
    "memory",
)

builder.add_edge(
    "memory",
    END,
)

chat_graph = builder.compile()
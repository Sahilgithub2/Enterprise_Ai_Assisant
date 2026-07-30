from app.services.ai_service import route_question


def router_node(state):

    tools = route_question(
        state["standalone_question"],
    )

    print("\n========== ROUTER ==========")
    print(tools)

    state["tools"] = tools

    return state
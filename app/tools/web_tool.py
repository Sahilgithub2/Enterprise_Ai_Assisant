from app.services.web_search_service import search_web


def get_web_context(
    question: str,
    previous_context: str = "",
):

    print("\n========== Web Search ==========\n")

    context = search_web(question)

    return {
        "context": context,
        "source": "Web Search",
    }
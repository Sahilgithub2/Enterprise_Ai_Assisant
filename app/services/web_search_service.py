from langchain_tavily import TavilySearch
from langchain_tavily import TavilySearch

from app.core.config import TAVILY_API_KEY

search_tool = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=5,
    topic="general",
    search_depth="advanced",
)

def search_web(query: str):
    response = search_tool.invoke(query)

    results = []

    for item in response.get("results", []):
        results.append(
            {
                "title": item.get("title"),
                "content": item.get("content"),
                "url": item.get("url"),
            }
        )

    formatted_results = []

    for index, result in enumerate(results, start=1):
        formatted_results.append(
        f"""
        Result {index}

        Title:
        {result["title"]}

        Content:
        {result["content"]}

        Source:
        {result["url"]}
        """
            )

        return "\n\n".join(formatted_results)

if __name__ == "__main__":
    result = search_web(
        "Latest Python version"
    )

    print(search_web("Latest Python version"))

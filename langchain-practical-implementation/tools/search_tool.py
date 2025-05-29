from langchain.tools import Tool

def fake_search(query: str) -> str:
    return f"Search results for '{query}': This is a simulated search result."

search_tool = Tool(
    name="Search",
    func=fake_search,
    description="Useful for answering general knowledge queries or current events."
)
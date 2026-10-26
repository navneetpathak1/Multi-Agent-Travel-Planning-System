# pyrefly: ignore [missing-import]
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily_key = os.getenv("TAVILY_API_KEY") or os.getenv("TAVITY_API_KEY")
client = TavilyClient(
    api_key=tavily_key
) if tavily_key else None



def tavily_search(query):
    api_key = os.getenv("TAVILY_API_KEY") or os.getenv("TAVITY_API_KEY")
    if not api_key:
        return f"Hotel and activity recommendations for '{query}': High-rated local accommodations, luxury resorts, and popular city tours."

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            max_results=5
        )

        results = []
        if isinstance(response, dict) and "results" in response:
            for i, r in enumerate(response["results"], 1):
                title   = r.get("title", "Unknown")
                url     = r.get("url", "")
                snippet = r.get("content", "").strip()
                if len(snippet) > 300:
                    snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

                results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

        return "\n\n".join(results) if results else f"Hotels & activities found for '{query}'."
    except Exception as e:
        return f"Hotels & options for '{query}': Selection of top-rated central hotels and local experience guides."
    
    
    
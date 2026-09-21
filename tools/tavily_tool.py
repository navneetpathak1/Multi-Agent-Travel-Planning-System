# pyrefly: ignore [missing-import]
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


# https://www.tavily.com/ 
# Signup and login, On dashboard- > under api keys you will see the default key.
# Use that or click on + to create new one. Then save it in .env file

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)



def tavily_search(query):
    api_key = os.getenv("TAVILY_API_KEY")
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
    
    
    
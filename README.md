# AI Travel Booking System

## Project Description

The **AI Travel Booking System** is an intelligent, multi-agent travel concierge that automates end-to-end trip planning from natural language queries. By breaking down the travel planning process into specialized autonomous agents, the system orchestrates real-time flight lookups, hotel and activity discovery, day-by-day itinerary generation, and comprehensive travel proposal synthesis. 

Each stage in the pipeline runs as an individual node within a directed agent graph. The system maintains conversation and state persistence across queries through database checkpointing, streams live agent progress to an interactive dark-mode dashboard, and automatically exports complete trip plans as downloadable Markdown files.

---

## Tech Stack

- **Agent Orchestration & Workflow**: [LangGraph](https://github.com/langchain-ai/langgraph) (`StateGraph`, `START`, `END`)
- **LLM Provider & Fast Inference**: [Groq](https://groq.com/) via `ChatGroq` (`langchain-groq`)
- **State Persistence & Memory**: [PostgreSQL](https://www.postgresql.org/) with `PostgresSaver` (`langgraph-checkpoint-postgres`, `psycopg`)
- **Frontend Dashboard**: [Streamlit](https://streamlit.io/) with custom responsive dark-theme CSS and live agent execution streaming
- **Web Search Engine**: [Tavily Search API](https://tavily.com/) (`tavily-python`) for real-time accommodations and activity recommendations
- **Flight Data API**: [AviationStack API](https://aviationstack.com/) for commercial airline routes and flight status retrieval
- **Core Runtime & Libraries**: Python 3, `python-dotenv`, `requests`, `pydantic`

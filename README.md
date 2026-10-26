# ✈️ AI Travel Booking System

An autonomous, multi-agent travel concierge that automates end-to-end trip planning from natural language queries. Built with **LangGraph**, **Groq**, **PostgreSQL**, and **Streamlit**, the system orchestrates real-time flight searches, accommodation discovery, day-by-day itinerary synthesis, and full travel proposal generation.

---

## 🌟 Key Features

- **Autonomous Multi-Agent Orchestration**: Sequential, specialized agents coordinate via a directed state graph.
- **Live Flight Lookups**: Commercial flight routes and status retrieved via the AviationStack API.
- **Curated Accommodations & Activities**: Real-time hotel, luxury resort, and local activity discovery via the Tavily Search API.
- **Fast LLM Inference**: Day-by-day scheduling and comprehensive proposal generation powered by Groq (`ChatGroq`).
- **State Persistence & Memory**: Checkpointed conversation state stored in PostgreSQL (`PostgresSaver`) across queries.
- **Streamlined Streamlit UI**:
  - Full-width modern dark mode interface with clean visual hierarchy.
  - Dedicated **Agent Pipeline** workflow overview card.
  - **Quick Prompt Chips**: Clickable vacation presets (e.g., Japan, Dubai, Paris & Switzerland under ₹10 Lakhs) that paste directly into the input area.
  - **Smart Prompt Enhancement**: Brief or empty prompts automatically default/enrich to a curated luxury vacation departing from India with a budget under ₹10 Lakhs (1,000,000 INR).
  - Live agent status updates during graph execution.
  - Downloadable Markdown itineraries with automatic auto-save to `travel_plans/`.

---

## 🤖 Agent Pipeline Architecture

```mermaid
flowchart LR
    START([START]) --> FA["① Flight Agent\n(AviationStack API)"]
    FA --> HA["② Hotel Agent\n(Tavily Search API)"]
    HA --> IA["③ Itinerary Agent\n(Groq LLM)"]
    IA --> RA["④ Final Agent\n(Groq LLM)"]
    RA --> END([END])
```

| Agent | Icon | Role & Responsibility |
| :--- | :---: | :--- |
| **Flight Agent** | ✈️ | Searches commercial airlines, departures, arrivals, and flight availability. |
| **Hotel Agent** | 🏨 | Discovers top-rated accommodations, luxury stays, and local points of interest. |
| **Itinerary Agent** | 🗓️ | Synthesizes a structured day-by-day schedule with balanced pacing and attractions. |
| **Final Agent** | 🧠 | Assembles flight, hotel, and itinerary data into an executive travel proposal aligned with user budget. |

---

## 🛠️ Tech Stack

- **Workflow Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph) (`StateGraph`, `START`, `END`)
- **LLM Provider**: [Groq](https://groq.com/) via `ChatGroq` (`langchain-groq`)
- **State Checkpointing**: [PostgreSQL](https://www.postgresql.org/) with `PostgresSaver` (`langgraph-checkpoint-postgres`, `psycopg`)
- **Frontend UI**: [Streamlit](https://streamlit.io/) with custom dark-mode CSS
- **Search & Retrieval**: [Tavily Search API](https://tavily.com/) (`tavily-python`)
- **Flight Data API**: [AviationStack API](https://aviationstack.com/)
- **Runtime**: Python 3.10+, `python-dotenv`, `requests`, `pydantic`

---

## 📁 Project Structure

```
├── .streamlit/
│   └── config.toml          # Streamlit configuration (telemetry disabled)
├── tools/
│   ├── flight_tool.py       # AviationStack flight search integration
│   └── tavily_tool.py       # Tavily web search integration for stays & tours
├── travel_plans/            # Directory containing generated itinerary Markdown files
├── .env                     # Environment variables and API keys
├── .gitignore               # Git ignored directories (.env, virtualenvs, plans)
├── frontend.py              # Streamlit web application and live pipeline UI
├── main.py                  # LangGraph state machine, agent nodes, and Postgres checkpointer
└── README.md                # Project documentation
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root with the following keys:

```env
# Groq API Key for LLM inference
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b

# AviationStack API Key for flight route queries
AVIATIONSTACK_API_KEY=your_aviationstack_key_here

# Tavily API Key for hotel & activity search
TAVILY_API_KEY=your_tavily_key_here

# PostgreSQL connection string for LangGraph checkpointing
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
```

---

## 🚀 Getting Started

### 1. Clone & Set Up Virtual Environment

```powershell
# Clone the repository
git clone https://github.com/navneetpathak1/Multi-Agent-Travel-Planning-System.git
cd Multi-Agent-Travel-Planning-System

# Create virtual environment
python -m venv langgraph_env3

# Activate virtual environment
# On Windows:
.\langgraph_env3\Scripts\activate
# On Linux/macOS:
source langgraph_env3/bin/activate
```

### 2. Install Dependencies

```powershell
pip install langgraph langchain-core langchain-groq langgraph-checkpoint-postgres psycopg tavily-python streamlit requests python-dotenv
```

### 3. Ensure PostgreSQL is Running

Make sure PostgreSQL is running and the database specified in your `DATABASE_URL` is accessible. LangGraph's `PostgresSaver` will automatically initialize checkpoint tables on startup.

---

## 🖥️ Running the Application

### Option A: Streamlit Interactive Web App (Recommended)

```powershell
streamlit run frontend.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

- Select a quick prompt or type your custom vacation request.
- Watch each agent execute live with intermediate status cards.
- View metrics (agents executed, LLM calls made).
- Download your complete itinerary as a Markdown document.

### Option B: Command Line Interface (CLI)

```powershell
python main.py
```
Enter your travel prompt interactively in the terminal and review the generated response.

---

## 📄 Output & Exports

All generated travel plans are automatically timestamped and archived under the `travel_plans/` folder:
- Example: `travel_plans/travel_plan_20261026_194500.md`
- Markdown files include sections for Flights, Hotels, Daily Itineraries, and the Final Synthesized Proposal.

import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from main import app

st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #080d14;
}

/* ── Completely remove sidebar ── */
section[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* ── Hero ── */
.hero-wrapper {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 1.6rem;
    height: 250px;
}
.hero-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.35);
    position: absolute;
    top: 0; left: 0;
}
.hero-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1.5rem 2rem;
}
.hero-badge {
    background: rgba(58,123,213,0.25);
    border: 1px solid rgba(58,123,213,0.5);
    color: #7ab8f5 !important;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 0.7rem;
    display: inline-block;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.5rem;
    line-height: 1.2;
}
.hero-sub {
    color: #94adc8;
    font-size: 0.95rem;
    max-width: 620px;
}

/* ── Agent Pipeline Card ── */
.pipeline-card {
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 16px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}
.pipeline-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.9rem;
}
.pipeline-badge {
    background: rgba(58,123,213,0.22);
    border: 1px solid rgba(58,123,213,0.45);
    color: #7ab8f5 !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
}
.pipeline-title {
    color: #e0edf8;
    font-size: 1.05rem;
    font-weight: 600;
}
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.9rem;
}
.pipeline-step {
    background: #09101b;
    border: 1px solid #17273c;
    border-radius: 12px;
    padding: 0.9rem 0.9rem;
    transition: all 0.2s ease;
}
.pipeline-step:hover {
    border-color: #3a7bd5;
    background: #0d1726;
    transform: translateY(-2px);
}
.step-badge {
    display: inline-block;
    color: #4ea8f0;
    font-weight: 700;
    font-size: 0.95rem;
    margin-right: 0.3rem;
}
.step-icon {
    font-size: 1.35rem;
    margin-bottom: 0.35rem;
}
.step-title {
    color: #ffffff;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.25rem;
}
.step-desc {
    color: #7a98b5;
    font-size: 0.78rem;
    line-height: 1.4;
}

/* ── Input card ── */
.input-label {
    color: #7ab8f5;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Primary Generate button ── */
button[kind="primary"] {
    background: linear-gradient(135deg, #1a6bbf 0%, #0d4a8a 50%, #0a3d75 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 0 24px rgba(26,107,191,0.35), 0 4px 15px rgba(0,0,0,0.4) !important;
    transition: all 0.3s ease !important;
}
button[kind="primary"]:hover {
    box-shadow: 0 0 40px rgba(26,107,191,0.6), 0 6px 20px rgba(0,0,0,0.5) !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #2278d4 0%, #1057a0 50%, #0d4a8a 100%) !important;
}
button[kind="primary"]:active {
    transform: translateY(0px) !important;
}

/* ── Secondary Quick prompt buttons ── */
button[kind="secondary"] {
    background: #0d1726 !important;
    color: #9ec5ed !important;
    border: 1px solid #1c324e !important;
    border-radius: 9px !important;
    padding: 0.45rem 0.65rem !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}
button[kind="secondary"]:hover {
    background: #14253d !important;
    color: #ffffff !important;
    border-color: #3a7bd5 !important;
    transform: translateY(-1px) !important;
}

/* ── Agent status cards ── */
[data-testid="stStatusWidget"] {
    background: #0e1a2e !important;
    border: 1px solid #1e3050 !important;
    border-radius: 12px !important;
}
[data-testid="stStatusWidget"] > div:first-child {
    background: #0e1a2e !important;
    border-radius: 12px 12px 0 0 !important;
}
[data-testid="stStatusWidget"] details,
[data-testid="stStatusWidget"] details > div,
[data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] {
    background: #0a1520 !important;
    color: #ffffff !important;
    padding: 0.25rem 0.5rem !important;
}
[data-testid="stStatusWidget"] * { color: #ffffff !important; }
[data-testid="stStatusWidget"] a { color: #4ea8f0 !important; }
[data-testid="stStatusWidget"] hr { border-color: #1e3050 !important; }

/* ── Section headers ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2e44;
}
.sec-head span { font-size: 1.15rem; font-weight: 600; color: #e0edf8; }

/* ── Metric bar ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-box {
    flex: 1;
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #4ea8f0; }
.metric-lbl { font-size: 0.78rem; color: #7aa8cc !important; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Final plan ── */
.final-card {
    background: linear-gradient(160deg, #0c1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3a5c;
    border-left: 4px solid #3a7bd5;
    border-radius: 14px;
    padding: 1.8rem;
    line-height: 1.8;
    color: #cce0f5;
    font-size: 0.95rem;
}

/* ── Save bar ── */
.save-bar {
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #8ab8d8 !important;
    font-size: 0.88rem;
    margin-top: 0.5rem;
}
.save-bar code { color: #7ab8f5 !important; background: #0a1520 !important; }

/* Hide branding */
#MainMenu, footer, header { visibility: hidden; }

/* Textarea */
.stTextArea textarea {
    background: #0a1520 !important;
    border: 1px solid #1e2e44 !important;
    border-radius: 10px !important;
    color: #e8f4ff !important;
    font-size: 0.95rem !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.2) !important;
}
.stTextArea textarea::placeholder { color: #4a6a85 !important; }

/* Text input */
input[type="text"], .stTextInput input {
    background: #0e1a2b !important;
    border: 1px solid #1a2e44 !important;
    border-radius: 8px !important;
    color: #e0edf8 !important;
}
input[type="text"]:focus, .stTextInput input:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.2) !important;
}
input[type="text"]::placeholder { color: #3a5570 !important; }

/* All Streamlit labels — dark bg → light text */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label {
    color: #7ab8f5 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
}

/* General markdown / paragraph text */
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {
    color: #cce0f5 !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e8f4ff !important; }
.stMarkdown code {
    background: #0e1a2b !important;
    color: #7ab8f5 !important;
    padding: 0.15em 0.4em;
    border-radius: 4px;
}

/* Alerts */
.stAlert { background: #0e1a2b !important; border-radius: 10px !important; }
.stAlert p, .stAlert div { color: #e0edf8 !important; }

/* Download button */
div[data-testid="stDownloadButton"] > button {
    background: #1a3a5c !important;
    color: #e8f4ff !important;
    border: 1px solid #2a5080 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state for user query and prompt pasting ────────────────────────────
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

def apply_quick_prompt(prompt_text: str):
    st.session_state.user_query = prompt_text

thread_id = "user_aarohi"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <img class="hero-bg"
         src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1400&q=80"
         alt="airplane above clouds"/>
    <div class="hero-content">
        <div class="hero-badge">✦ Multi-Agent AI System</div>
        <div class="hero-title">✈️ AI Travel Booking System</div>
        <div class="hero-sub">Autonomous multi-agent concierge searching flights, discovering stays, crafting day-by-day itineraries, and delivering complete travel plans.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Destination image strip ───────────────────────────────────────────────────
DESTINATIONS = [
    ("🇯🇵 Tokyo",     "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇫🇷 Paris",     "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),
    ("🇹🇭 Bangkok",   "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),
    ("🇮🇹 Rome",      "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70"),
    ("🇦🇪 Dubai",     "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]

cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(f"""
        <div style="border-radius:10px;overflow:hidden;position:relative;height:85px;margin-bottom:1rem;">
            <img src="{img_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.55);" />
            <div style="position:absolute;bottom:8px;left:0;right:0;text-align:center;
                        color:#fff;font-size:0.8rem;font-weight:600;">{name}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Card for Agent Pipeline (Before Describe Your Trip) ─────────────────────────
st.markdown("""
<div class="pipeline-card">
    <div class="pipeline-header">
        <span class="pipeline-badge">⚡ Workflow</span>
        <span class="pipeline-title">Agent Pipeline</span>
    </div>
    <div class="pipeline-grid">
        <div class="pipeline-step">
            <div class="step-icon">✈️</div>
            <div class="step-title"><span class="step-badge">①</span> Flight Agent</div>
            <div class="step-desc">Searches live commercial airline routes and departure/arrival schedules</div>
        </div>
        <div class="pipeline-step">
            <div class="step-icon">🏨</div>
            <div class="step-title"><span class="step-badge">②</span> Hotel Agent</div>
            <div class="step-desc">Discovers top-rated accommodations, luxury resorts, and popular attractions</div>
        </div>
        <div class="pipeline-step">
            <div class="step-icon">🗓️</div>
            <div class="step-title"><span class="step-badge">③</span> Itinerary Agent</div>
            <div class="step-desc">Synthesizes day-by-day pacing, travel schedule, and sightseeing activities</div>
        </div>
        <div class="pipeline-step">
            <div class="step-icon">🧠</div>
            <div class="step-title"><span class="step-badge">④</span> Final Agent</div>
            <div class="step-desc">Consolidates flights, hotels, and schedule into a cohesive final proposal</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Describe Your Trip Section ─────────────────────────────────────────────────
st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)

user_query = st.text_area(
    "Describe your trip",
    key="user_query",
    placeholder="e.g. Plan a 7-day luxury trip to Japan from Mumbai under ₹10 lakhs with flights, 5-star hotels, and bullet trains...",
    height=110,
    label_visibility="collapsed",
)

st.markdown("<div style='color:#7ab8f5; font-size:0.78rem; font-weight:600; letter-spacing:0.06em; margin:0.3rem 0 0.4rem;'>⚡ QUICK PROMPTS (Click to paste into input box):</div>", unsafe_allow_html=True)

QUICK_PROMPTS = [
    ("🇯🇵 Japan (₹10L)", "Plan a complete 7-day luxury trip to Japan from Mumbai under ₹10 lakhs including round-trip flights, 5-star hotels in Tokyo and Kyoto, bullet train passes, and curated sightseeing."),
    ("🇫🇷 Paris & Swiss (₹10L)", "Plan an 8-day Paris and Switzerland vacation from Delhi under ₹10 lakhs with 5-star stays, scenic train passes, Eiffel Tower dinner, and guided tours."),
    ("🇦🇪 Dubai VIP (₹10L)", "Plan a 6-day ultra-luxury Dubai holiday from India under ₹10 lakhs with Emirates flights, Atlantis The Palm stay, private desert safari, and yacht tour."),
    ("🏝️ Bali Luxury (₹10L)", "Plan a 7-day luxury honeymoon in Bali from Bangalore under ₹10 lakhs including private pool villa, flights, and island excursions."),
    ("🇮🇳 Royal Rajasthan (₹10L)", "Plan a 7-day ultra-luxury royal heritage tour of Udaipur and Jaipur under ₹10 lakhs from Mumbai staying at Taj Lake Palace and Rambagh Palace with private chauffeur.")
]

qcols = st.columns(len(QUICK_PROMPTS))
for qc, (label, prompt_text) in zip(qcols, QUICK_PROMPTS):
    with qc:
        st.button(
            label,
            key=f"qp_{label}",
            on_click=apply_quick_prompt,
            args=(prompt_text,),
            type="secondary",
            use_container_width=True
        )

st.markdown("<br>", unsafe_allow_html=True)
generate = st.button("🚀  Generate My Travel Plan", type="primary", use_container_width=True)

# ── Agent Execution Pipeline ──────────────────────────────────────────────────
AGENT_META = {
    "flight_agent":    ("✈️", "Flight Agent"),
    "hotel_agent":     ("🏨", "Hotel Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
    "final_agent":     ("🧠", "Final Agent"),
}

if generate:
    raw_query = st.session_state.get("user_query", "").strip()

    # If user prompt is empty or not detailed enough, default to trip from India under 10 lakhs rupees
    if not raw_query:
        effective_query = (
            "Plan a comprehensive 7-day luxury vacation departing from India under ₹10 lakhs (INR) budget "
            "including return flights from Mumbai/Delhi, premium 5-star hotel accommodations, daily activities, "
            "and a detailed day-by-day itinerary."
        )
        st.info("💡 No prompt provided — automatically generated a curated luxury trip from India under ₹10 lakhs!")
    elif len(raw_query.split()) < 4 or ("india" not in raw_query.lower() and "lakh" not in raw_query.lower() and "10" not in raw_query.lower()):
        effective_query = (
            f"{raw_query}. Please plan this complete trip departing from India with a total budget under ₹10 lakhs "
            f"(1,000,000 INR), including return flights from India, 4 to 5-star hotel accommodations, "
            f"local sightseeing experiences, and a structured day-by-day itinerary."
        )
        st.info("💡 Enriched your trip prompt: departing from India under ₹10 lakhs budget.")
    else:
        effective_query = raw_query

    config = {"configurable": {"thread_id": thread_id}}
    collected = {
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "final_response": "",
        "llm_calls": 0,
    }

    st.markdown("---")
    st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline — Live</span></div>", unsafe_allow_html=True)

    for chunk in app.stream(
        {
            "messages": [HumanMessage(content=effective_query)],
            "user_query": effective_query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
        },
        config=config,
        stream_mode="updates",
    ):
        for node_name, state_update in chunk.items():
            icon, label = AGENT_META.get(node_name, ("🔧", node_name))

            with st.status(f"{icon}  {label}", state="complete", expanded=True):
                if node_name == "flight_agent":
                    text = state_update.get("flight_results", "")
                    collected["flight_results"] = text
                    st.markdown(text or "_No flight data returned._")

                elif node_name == "hotel_agent":
                    text = state_update.get("hotel_results", "")
                    collected["hotel_results"] = text
                    st.markdown(text or "_No hotel data returned._")

                elif node_name == "itinerary_agent":
                    text = state_update.get("itinerary", "")
                    collected["itinerary"] = text
                    st.markdown(text or "_No itinerary generated._")

                elif node_name == "final_agent":
                    msgs = state_update.get("messages", [])
                    text = msgs[-1].content if msgs else ""
                    collected["final_response"] = text
                    st.markdown(text or "_No final response._")

                collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

    # Metrics
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Agents Run</div></div>
        <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls</div></div>
        <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Status</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Final plan card
    if collected["final_response"]:
        st.markdown("<div class='sec-head'><span>🧠 Final Travel Plan</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='final-card'>{collected['final_response']}</div>", unsafe_allow_html=True)

    # Save Markdown file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"travel_plan_{timestamp}.md"
    save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
    os.makedirs(save_dir, exist_ok=True)

    file_content = f"""# Travel Plan
**Query:** {effective_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User ID:** {thread_id}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## 🗓️ Itinerary
{collected['itinerary'] or 'N/A'}

---

## 🧠 Final Travel Plan
{collected['final_response'] or 'N/A'}

---
*LLM Calls: {collected['llm_calls']}*
"""
    with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
        f.write(file_content)

    dl_col, info_col = st.columns([1, 3])
    with dl_col:
        st.download_button(
            "⬇️ Download Plan",
            data=file_content,
            file_name=filename,
            mime="text/markdown",
            use_container_width=True,
        )
    with info_col:
        st.markdown(f"<div class='save-bar'>📁 Auto-saved → <code>travel_plans/{filename}</code></div>", unsafe_allow_html=True)
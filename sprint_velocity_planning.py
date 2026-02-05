"""
Sprint Velocity Planning - Streamlit App with Supabase
CHG Web Product Team

To run locally: streamlit run sprint_velocity_planning.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from supabase import create_client
import os

# ============== PAGE CONFIG ==============
st.set_page_config(
    page_title="Sprint Velocity Planning",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============== SUPABASE CONNECTION ==============
SUPABASE_URL = "https://iwarvepodaijjofyyvvm.supabase.co"
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3YXJ2ZXBvZGFpampvZnl5dnZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzMDQyOTksImV4cCI6MjA4NTg4MDI5OX0.z9c_aYcY53G7Id3FSyNgrheNtKVWlSt5EGaoM-wAMWc"))

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# ============== CUSTOM CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Root overrides */
    :root {
        --primary-color: #4a5d4a;
        --background-color: #f5f5f0;
        --text-color: #3d3d3d;
    }

    /* Base styling */
    html, body, .main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: #f5f5f0 !important;
    }

    .stApp > header {
        background: transparent !important;
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton, [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Main container - constrain width */
    .block-container {
        max-width: 900px !important;
        padding: 2rem 1rem 4rem 1rem !important;
    }

    /* Typography - no pure black anywhere, soft grays like Pointing Poker */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Main text - soft dark gray, never black */
    h1, h2, h3, h4, h5, h6 {
        color: #4a4a4a !important;
    }

    p, span, div, .stMarkdown, .stText {
        color: #5a5a5a !important;
    }

    /* Bold/strong text - still soft */
    strong, b {
        color: #4a4a4a !important;
    }

    /* Labels and secondary text */
    label, .stTextInput > label, .stNumberInput > label, .stSelectbox > label, .stDateInput > label {
        color: #8a8a8a !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Input text - soft gray, not black */
    input, textarea, select, [data-baseweb="input"] input {
        color: #4a4a4a !important;
    }

    /* Header */
    .app-header {
        text-align: center;
        padding: 32px 0 24px 0;
        margin-bottom: 8px;
    }

    .app-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #4a4a4a !important;
        letter-spacing: -0.01em;
        margin: 0;
    }

    .app-subtitle {
        color: #9a9a9a !important;
        font-size: 0.85rem;
        font-weight: 400;
        margin-top: 8px;
        letter-spacing: 0.02em;
    }

    /* Section labels */
    .section-label {
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8a8a8a !important;
        margin-bottom: 8px;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #4a4a4a !important;
        margin: 0 0 16px 0;
    }

    /* Tabs - minimal underline style */
    .stTabs {
        margin-bottom: 24px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent !important;
        border-bottom: 1px solid #e0e0db;
        justify-content: center;
        padding: 0;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        color: #8a8a8a !important;
        border-bottom: 2px solid transparent !important;
        margin-bottom: -1px;
    }

    .stTabs [aria-selected="true"] {
        color: #4a5d4a !important;
        border-bottom: 2px solid #4a5d4a !important;
        background: transparent !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #4a5d4a !important;
        background: transparent !important;
    }

    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* Cards - cream background, not white */
    .card {
        background: #faf9f6;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #e8e8e3;
    }

    /* Team cards with left border */
    .team-card {
        background: #faf9f6;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
        border: 1px solid #e8e8e3;
        border-left: 3px solid #6b7c6b;
    }

    /* All teams use same sage green accent */
    .team-card.orange { border-left-color: #4a5d4a; }
    .team-card.green { border-left-color: #4a5d4a; }
    .team-card.cyan { border-left-color: #4a5d4a; }

    /* Team header */
    .team-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .team-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #3d3d3d !important;
        margin: 0;
    }

    /* All team names use same color */
    .team-name.orange { color: #3d4d3d !important; }
    .team-name.green { color: #3d4d3d !important; }
    .team-name.cyan { color: #3d4d3d !important; }

    .team-meta {
        font-size: 0.75rem;
        color: #8a8a8a !important;
        margin-top: 2px;
    }

    .team-badge {
        font-size: 0.7rem;
        font-weight: 500;
        color: #4a5d4a !important;
        background: #e8efe8;
        padding: 4px 10px;
        border-radius: 12px;
    }

    /* Developer rows */
    .dev-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0eb;
    }

    .dev-row:last-child {
        border-bottom: none;
    }

    .dev-name {
        font-size: 0.85rem;
        font-weight: 500;
        color: #2d2d2d !important;
    }

    /* Buttons - dark sage with WHITE text (high contrast, accessible) */
    .stButton > button,
    .stFormSubmitButton > button,
    [data-testid="stFormSubmitButton"] > button,
    button[kind="primary"],
    button[kind="primaryFormSubmit"] {
        background: #4a5d4a !important;
        background-color: #4a5d4a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: background 0.2s !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        background: #3d4d3d !important;
        background-color: #3d4d3d !important;
        color: #ffffff !important;
    }

    .stButton > button:active, .stButton > button:focus,
    .stFormSubmitButton > button:active, .stFormSubmitButton > button:focus {
        background: #3d4d3d !important;
        background-color: #3d4d3d !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }

    .stButton > button *,
    .stFormSubmitButton > button * {
        color: #ffffff !important;
    }

    /* ======== NUMBER INPUTS ======== */
    /* Container - no extra borders */
    .stNumberInput > div > div {
        border: none !important;
        box-shadow: none !important;
    }

    /* Input wrapper */
    .stNumberInput [data-baseweb="input"] {
        background: #faf9f6 !important;
        border: 1px solid #e0e0db !important;
        border-radius: 8px !important;
    }

    /* Text field */
    .stNumberInput input {
        background: transparent !important;
        color: #4a4a4a !important;
        text-align: center !important;
    }

    /* Focus */
    .stNumberInput [data-baseweb="input"]:focus-within {
        border-color: #6b7c6b !important;
        box-shadow: 0 0 0 2px rgba(107, 124, 107, 0.15) !important;
    }

    /* ======== SELECT BOXES / DROPDOWNS ======== */
    /* Remove outer container borders */
    .stSelectbox > div {
        border: none !important;
        box-shadow: none !important;
    }
    .stSelectbox > div > div {
        border: none !important;
        box-shadow: none !important;
    }

    .stSelectbox [data-baseweb="select"] {
        background: #faf9f6 !important;
        border: 1px solid #e5e5e0 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: #faf9f6 !important;
        color: #4a4a4a !important;
        border: none !important;
    }

    /* Override red focus - sage green */
    .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #4a5d4a !important;
        box-shadow: 0 0 0 1px #4a5d4a !important;
    }

    .stSelectbox svg {
        fill: #7a7a7a !important;
    }

    /* ======== DROPDOWN MENUS - AGGRESSIVE LIGHT BACKGROUND ======== */
    /* Target ALL popover and menu elements globally */
    [data-baseweb="popover"],
    [data-baseweb="popover"] *,
    [data-baseweb="menu"],
    [data-baseweb="menu"] *,
    [data-baseweb="list"],
    [data-baseweb="list"] *,
    ul[role="listbox"],
    ul[role="listbox"] *,
    div[role="listbox"],
    div[role="listbox"] * {
        background: #faf9f6 !important;
        background-color: #faf9f6 !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        border: 1px solid #e5e5e0 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }

    /* Option items text color */
    [data-baseweb="menu"] li,
    ul[role="listbox"] li,
    div[role="listbox"] div[role="option"],
    [data-baseweb="menu"] [role="option"],
    [role="option"],
    [role="option"] * {
        background: #faf9f6 !important;
        background-color: #faf9f6 !important;
        color: #4a4a4a !important;
    }

    /* Hover states */
    [data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover,
    div[role="listbox"] div[role="option"]:hover,
    [data-baseweb="menu"] [role="option"]:hover,
    [role="option"]:hover,
    [data-highlighted="true"],
    [data-highlighted="true"] * {
        background: #f0efec !important;
        background-color: #f0efec !important;
    }

    /* Selected option styling */
    [aria-selected="true"],
    [aria-selected="true"] *,
    [data-baseweb="menu"] li[aria-selected="true"] {
        background: #e8efe8 !important;
        background-color: #e8efe8 !important;
        color: #3d4d3d !important;
    }

    /* Override any inline dark backgrounds on body popover portals */
    body > div[data-baseweb] {
        background: transparent !important;
    }

    body > div[data-baseweb] > div {
        background: #faf9f6 !important;
    }

    /* ======== DATE INPUTS ======== */
    .stDateInput > div {
        border: none !important;
        box-shadow: none !important;
    }
    .stDateInput > div > div {
        border: none !important;
        box-shadow: none !important;
    }

    .stDateInput [data-baseweb="input"] {
        background: #faf9f6 !important;
        border: 1px solid #e5e5e0 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
    }

    .stDateInput input {
        background: #faf9f6 !important;
        color: #4a4a4a !important;
        border: none !important;
    }

    .stDateInput [data-baseweb="input"]:focus-within {
        border-color: #4a5d4a !important;
        box-shadow: 0 0 0 1px #4a5d4a !important;
    }

    .stDateInput svg {
        fill: #7a7a7a !important;
    }

    /* Date picker calendar popup */
    [data-baseweb="calendar"],
    [data-baseweb="datepicker"] {
        background: #faf9f6 !important;
        border: 1px solid #e5e5e0 !important;
    }

    [data-baseweb="calendar"] * {
        color: #4a4a4a !important;
    }

    /* Calendar selected day - sage green */
    [data-baseweb="calendar"] [aria-selected="true"],
    [data-baseweb="calendar"] div[aria-selected="true"] {
        background: #4a5d4a !important;
        color: #fff !important;
    }

    /* ======== TEXT INPUTS ======== */
    .stTextInput > div {
        border: none !important;
        box-shadow: none !important;
    }
    .stTextInput > div > div {
        border: none !important;
        box-shadow: none !important;
    }

    .stTextInput input {
        background: #faf9f6 !important;
        border: 1px solid #e5e5e0 !important;
        border-radius: 6px !important;
        color: #4a4a4a !important;
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
        box-shadow: none !important;
    }

    .stTextInput input:focus {
        border-color: #4a5d4a !important;
        box-shadow: 0 0 0 1px #4a5d4a !important;
    }

    /* Metric cards - cream */
    .metric-card {
        background: #faf9f6;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        border: 1px solid #e8e8e3;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3d3d3d !important;
        line-height: 1.2;
        margin: 4px 0;
    }

    /* All metric values use consistent sage green */
    .metric-value.orange { color: #3d4d3d !important; }
    .metric-value.green { color: #3d4d3d !important; }
    .metric-value.cyan { color: #3d4d3d !important; }

    .metric-label {
        font-size: 0.65rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #7a7a7a !important;
    }

    .metric-sub {
        font-size: 0.75rem;
        color: #8a8a8a !important;
    }

    /* Forecast cards - cream */
    .forecast-card {
        background: #faf9f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e8e8e3;
        margin-bottom: 12px;
    }

    .forecast-team {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }

    .forecast-raw {
        font-size: 0.8rem;
        color: #8a8a8a !important;
        margin-bottom: 8px;
    }

    .forecast-value {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 4px;
    }

    .forecast-buffer {
        font-size: 0.7rem;
        color: #8a8a8a !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Breakdown items */
    .breakdown-item {
        background: #f8f8f5;
        border-radius: 6px;
        padding: 10px 12px;
        margin-top: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .breakdown-name {
        font-size: 0.85rem;
        font-weight: 500;
        color: #3d3d3d !important;
    }

    .breakdown-meta {
        font-size: 0.7rem;
        color: #8a8a8a !important;
        margin-top: 1px;
    }

    .breakdown-value {
        font-size: 1rem;
        font-weight: 700;
        color: #3d3d3d !important;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #e5e5e0;
        margin: 20px 0;
    }

    /* Info/alert boxes */
    .stAlert {
        background: #fafaf8 !important;
        border: 1px solid #e5e5e0 !important;
        border-radius: 6px !important;
    }

    .stAlert > div {
        color: #555 !important;
    }

    /* Expanders - subtle styling */
    .streamlit-expanderHeader {
        background: transparent !important;
        border: none !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        color: #7a7a7a !important;
        padding: 8px 0 !important;
    }

    .streamlit-expanderHeader:hover {
        color: #4a5d4a !important;
    }

    .streamlit-expanderContent {
        border: none !important;
        padding: 8px 0 !important;
    }

    [data-testid="stExpander"] {
        border: none !important;
        background: transparent !important;
    }

    [data-testid="stExpander"] summary {
        font-size: 0.75rem !important;
        color: #8a8a8a !important;
    }

    [data-testid="stExpander"] summary:hover {
        color: #6b7c6b !important;
    }

    /* ======== DATA TABLES ======== */
    .stDataFrame,
    [data-testid="stDataFrame"] {
        border-radius: 8px;
    }

    /* Column gap fix */
    [data-testid="column"] {
        padding: 0 8px;
    }

    /* ======== BALANCED SPACING ======== */
    /* Clean but not cramped */
    .stMarkdown {
        margin-bottom: 0 !important;
    }

    /* Dividers - proper breathing room */
    hr {
        margin: 16px 0 !important;
    }

    /* Vertical block spacing - balanced */
    [data-testid="stVerticalBlock"] > div {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.75rem !important;
    }

    /* Tab content padding */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 16px !important;
    }

    /* Form elements - slight margin */
    .stSelectbox, .stNumberInput, .stTextInput, .stDateInput {
        margin-bottom: 6px !important;
    }

    /* Element containers */
    [data-testid="element-container"] {
        margin-bottom: 4px !important;
    }

    /* Horizontal layouts */
    [data-testid="stHorizontalBlock"] {
        gap: 8px !important;
    }

    /* Column inner spacing */
    [data-testid="stColumn"] > div {
        gap: 4px !important;
    }

    /* Form containers */
    .stForm {
        padding: 0 !important;
    }

    [data-testid="stForm"] > div {
        gap: 0.75rem !important;
    }

    /* Developer row styling - add visual separation */
    .dev-row-container {
        padding: 10px 0;
        border-bottom: 1px solid #f0efec;
    }

    .dev-row-container:last-child {
        border-bottom: none;
    }

    /* ======== PLOTLY CHARTS ======== */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }

    /* Make chart text readable */
    .js-plotly-plot .plotly text {
        fill: #5a5a5a !important;
    }

    .js-plotly-plot .plotly .gtitle,
    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle {
        fill: #5a5a5a !important;
    }

    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {
        fill: #6a6a6a !important;
    }

    .js-plotly-plot .plotly .legend text {
        fill: #5a5a5a !important;
    }
</style>
""", unsafe_allow_html=True)

# ============== DATA DEFINITIONS ==============
DEVELOPERS = [
    {"id": "brady-hession", "name": "Brady Hession", "role": "Software Engineer II"},
    {"id": "cody-worthen", "name": "Cody Worthen", "role": "Software Engineer II"},
    {"id": "fernando-fernandez", "name": "Fernando Fernandez", "role": "Software Engineer II"},
    {"id": "fredrik-svensson", "name": "Fredrik Svensson", "role": "Sr. Software Engineer"},
    {"id": "jaime-virrueta", "name": "Jaime Virrueta", "role": "Software Engineer (Globant)"},
    {"id": "matthew-callison", "name": "Matthew Callison", "role": "Software Engineer II"},
    {"id": "stephen-corry", "name": "Stephen Corry", "role": "Software Engineer II"},
    {"id": "tom-sharrock", "name": "Tom Sharrock", "role": "Staff Engineer"},
]

TEAMS = [
    {"id": "team1", "name": "Team 1", "displayName": "Web Team 1", "pmName": "Jason and Spencer", "color": "orange"},
    {"id": "team2", "name": "Team 2", "displayName": "Web Team 2", "pmName": "Matt and Matt", "color": "green"},
    {"id": "storyblok", "name": "Storyblok", "displayName": "Storyblok Team", "pmName": "Storyblok", "color": "cyan"},
]

# All teams use consistent sage green
TEAM_COLORS = {"orange": "#4a5d4a", "green": "#4a5d4a", "cyan": "#4a5d4a"}

HOLIDAYS = [
    {"name": "New Year's Day", "month": 1, "day": 1, "type": "full-day"},
    {"name": "MLK Day", "month": 1, "pattern": "third-monday", "type": "full-day"},
    {"name": "Memorial Day", "month": 5, "pattern": "last-monday", "type": "full-day"},
    {"name": "Independence Day", "month": 7, "day": 4, "type": "full-day"},
    {"name": "Labor Day", "month": 9, "pattern": "first-monday", "type": "full-day"},
    {"name": "Thanksgiving", "month": 11, "pattern": "fourth-thursday", "type": "full-day"},
    {"name": "Day after Thanksgiving", "month": 11, "pattern": "fourth-friday", "type": "full-day"},
    {"name": "Christmas Eve", "month": 12, "day": 24, "type": "half-day"},
    {"name": "Christmas Day", "month": 12, "day": 25, "type": "full-day"},
    {"name": "New Year's Eve", "month": 12, "day": 31, "type": "half-day"},
]

# ============== DATABASE FUNCTIONS ==============
def load_sprints():
    try:
        result = supabase.table("sprints").select("*").order("start_date", desc=True).execute()
        sprints = []
        for s in result.data:
            assignments = supabase.table("sprint_assignments").select("*").eq("sprint_id", s["sprint_id"]).execute()
            sprints.append({
                "sprintId": s["sprint_id"],
                "sprintName": s["sprint_name"],
                "startDate": s["start_date"],
                "endDate": s["end_date"],
                "sprintDays": s["sprint_days"],
                "assignments": [{
                    "engineerId": a["engineer_id"],
                    "teamId": a["team_id"],
                    "storyPoints": float(a["story_points"]),
                    "totalPtoDays": float(a["pto_days"])
                } for a in assignments.data]
            })
        return sprints
    except Exception as e:
        st.error(f"Error loading sprints: {e}")
        return []

def save_sprint(sprint_data):
    try:
        supabase.table("sprints").insert({
            "sprint_id": sprint_data["sprintId"],
            "sprint_name": sprint_data["sprintName"],
            "start_date": sprint_data["startDate"],
            "end_date": sprint_data["endDate"],
            "sprint_days": sprint_data["sprintDays"]
        }).execute()

        for a in sprint_data["assignments"]:
            supabase.table("sprint_assignments").insert({
                "sprint_id": sprint_data["sprintId"],
                "engineer_id": a["engineerId"],
                "team_id": a["teamId"],
                "story_points": a["storyPoints"],
                "pto_days": a["totalPtoDays"]
            }).execute()
        return True
    except Exception as e:
        st.error(f"Error saving sprint: {e}")
        return False

def load_team_assignments():
    try:
        result = supabase.table("team_assignments").select("*").execute()
        if result.data:
            return {row["engineer_id"]: row["team_id"] for row in result.data}
    except:
        pass
    # Default assignments
    return {
        "fredrik-svensson": "team1", "fernando-fernandez": "team1",
        "matthew-callison": "team1", "cody-worthen": "team1",
        "stephen-corry": "team2", "tom-sharrock": "team2",
        "brady-hession": "team2", "jaime-virrueta": "team2"
    }

def update_team_assignment(engineer_id, team_id):
    try:
        # Delete existing assignment first, then insert new one
        supabase.table("team_assignments").delete().eq("engineer_id", engineer_id).execute()
        supabase.table("team_assignments").insert({
            "engineer_id": engineer_id,
            "team_id": team_id
        }).execute()
    except Exception as e:
        st.error(f"Error updating team: {e}")

# ============== UTILITY FUNCTIONS ==============
def calculate_holiday_date(year, month, pattern):
    d = date(year, month, 1)
    if pattern == "third-monday":
        count = 0
        while count < 3:
            if d.weekday() == 0: count += 1
            if count < 3: d += timedelta(days=1)
    elif pattern == "last-monday":
        d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year + 1, 1, 1) - timedelta(days=1)
        while d.weekday() != 0: d -= timedelta(days=1)
    elif pattern == "first-monday":
        while d.weekday() != 0: d += timedelta(days=1)
    elif pattern == "fourth-thursday":
        count = 0
        while count < 4:
            if d.weekday() == 3: count += 1
            if count < 4: d += timedelta(days=1)
    elif pattern == "fourth-friday":
        temp = date(year, month, 1)
        count = 0
        while count < 4:
            if temp.weekday() == 3: count += 1
            if count < 4: temp += timedelta(days=1)
        d = temp + timedelta(days=1)
    return d

def get_holidays_in_range(start_date, end_date):
    if isinstance(start_date, str): start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str): end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    holidays = []
    for h in HOLIDAYS:
        hd = date(start_date.year, h["month"], h["day"]) if h.get("day") else calculate_holiday_date(start_date.year, h["month"], h.get("pattern"))
        if hd and start_date <= hd <= end_date:
            holidays.append(h)
    return holidays

def round_to_half(num): return round(num * 2) / 2

def calculate_velocity(assignments, lookback=10):
    valid = [a for a in assignments if a.get("storyPoints", 0) > 0]
    if not valid: return 0
    weights = {"recent": 0.50, "midRange": 0.30, "older": 0.15, "oldest": 0.05}
    total_wv, total_w = 0, 0
    for i, a in enumerate(valid[:lookback]):
        hd = sum(1 if h["type"] == "full-day" else 0.5 for h in get_holidays_in_range(a.get("startDate", ""), a.get("endDate", ""))) if a.get("startDate") else 0
        wd = a.get("sprintDays", 10) - a.get("totalPtoDays", 0) - hd
        v = a["storyPoints"] / wd if wd > 0 else 0
        n = i + 1
        w = weights["recent"]/3 if n <= 3 else weights["midRange"]/3 if n <= 6 else weights["older"]/3 if n <= 9 else weights["oldest"]/(lookback-9) if lookback > 9 else 0
        total_wv += v * w
        total_w += w
    return total_wv / total_w if total_w > 0 else 0

# ============== SESSION STATE ==============
if "pto_data" not in st.session_state: st.session_state.pto_data = {}
if "forecast" not in st.session_state: st.session_state.forecast = None
if "planning_buffer" not in st.session_state: st.session_state.planning_buffer = 0.85

# ============== VIEWS ==============
def render_forecast():
    team_assignments = load_team_assignments()
    sprints = load_sprints()

    # Buffer + Calculate row
    col1, col2 = st.columns([3, 1])
    with col1:
        buffer_opts = {"85% (Standard)": 0.85, "70% (Conservative)": 0.70, "100% (Aggressive)": 1.00}
        sel = st.selectbox("Planning Buffer", list(buffer_opts.keys()), index=0)
        st.session_state.planning_buffer = buffer_opts[sel]
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        calc = st.button("Calculate", type="primary", use_container_width=True)

    st.markdown("---")

    # 3-column layout for teams
    col1, col2, col3 = st.columns(3)

    def render_team_column(team, devs):
        """Render a team's card and developer list"""
        # Team header card
        st.markdown(f'''
        <div style="background:#faf9f6; border-radius:10px; padding:14px 16px; margin-bottom:12px; border:1px solid #e5e5e0; border-left:3px solid #6b7c6b;">
            <div style="font-size:0.9rem; font-weight:600; color:#4a4a4a; margin-bottom:2px;">{team['name']}</div>
            <div style="font-size:0.7rem; color:#8a8a8a;">{team['pmName']} · {len(devs)} devs</div>
        </div>
        ''', unsafe_allow_html=True)

        if devs:
            for dev in devs:
                st.markdown(f"**{dev['name']}**")
                pto = st.number_input("PTO Days", 0.0, 10.0, st.session_state.pto_data.get(dev["id"], 0.0), 0.5, key=f"pto_{dev['id']}")
                st.session_state.pto_data[dev["id"]] = pto
                other_teams = [t for t in TEAMS if t["id"] != team["id"]]
                mv = st.selectbox("Move to", ["—"] + [t["name"] for t in other_teams], key=f"mv_{dev['id']}")
                if mv != "—":
                    update_team_assignment(dev["id"], next(t["id"] for t in other_teams if t["name"] == mv))
                    st.rerun()
        else:
            st.markdown("*No developers*")

    with col1:
        team1 = TEAMS[0]
        team1_devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team1["id"]]
        render_team_column(team1, team1_devs)

    with col2:
        team2 = TEAMS[1]
        team2_devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team2["id"]]
        render_team_column(team2, team2_devs)

    with col3:
        team3 = TEAMS[2]
        team3_devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team3["id"]]
        render_team_column(team3, team3_devs)

    if calc:
        buf = st.session_state.planning_buffer
        results = {}
        for team in TEAMS:
            devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team["id"]]
            assigns = []
            for dev in devs:
                dev_sp = [{**a, "sprintDays": s["sprintDays"], "startDate": s["startDate"], "endDate": s["endDate"]}
                          for s in sprints for a in s.get("assignments", []) if a["engineerId"] == dev["id"]]
                vel = calculate_velocity(dev_sp)
                pto = st.session_state.pto_data.get(dev["id"], 0)
                raw = vel * (10 - pto)
                assigns.append({"name": dev["name"], "vel": vel, "pto": pto, "wd": 10-pto, "raw": raw, "buf": round_to_half(raw * buf)})
            results[team["id"]] = {"name": team["displayName"], "color": team["color"], "assigns": assigns,
                                   "raw": sum(a["raw"] for a in assigns), "buf": round_to_half(sum(a["buf"] for a in assigns))}
        st.session_state.forecast = {"buffer": buf, "teams": results}

    if st.session_state.forecast:
        st.markdown("---")
        st.markdown('<p class="section-label">Forecast Results</p>', unsafe_allow_html=True)

        f = st.session_state.forecast
        cols = st.columns(3)
        for idx, team in enumerate(TEAMS):
            r = f["teams"].get(team["id"], {})
            color = TEAM_COLORS.get(r.get("color", "green"), "#5d6b5d")
            with cols[idx]:
                st.markdown(f'''
                <div class="forecast-card">
                    <div class="forecast-team" style="color:{color};">{r.get('name', team['name'])}</div>
                    <div class="forecast-raw">Raw: {r.get('raw', 0):.1f} pts</div>
                    <div class="forecast-value" style="color:{color};">{r.get('buf', 0):.1f}</div>
                    <div class="forecast-buffer">{int(f['buffer']*100)}% buffer</div>
                </div>
                ''', unsafe_allow_html=True)

                for a in r.get("assigns", []):
                    st.markdown(f'''
                    <div class="breakdown-item">
                        <div>
                            <div class="breakdown-name">{a['name']}</div>
                            <div class="breakdown-meta">{a['vel']:.2f} pts/day · {a['wd']:.0f} days</div>
                        </div>
                        <div class="breakdown-value">{a['buf']:.1f}</div>
                    </div>
                    ''', unsafe_allow_html=True)

def render_add_sprint():
    team_assignments = load_team_assignments()

    with st.form("add_sprint"):
        c1, c2, c3 = st.columns(3)
        with c1: name = st.text_input("Sprint Name", placeholder="e.g., Suttungr")
        with c2: start = st.date_input("Start Date")
        with c3: end = st.date_input("End Date", value=date.today() + timedelta(days=13))

        if start and end:
            hols = get_holidays_in_range(start, end)
            if hols: st.info(f"Holidays: {', '.join(h['name'] for h in hols)}")

        st.markdown("---")
        st.markdown('<p class="section-label">Developer Points</p>', unsafe_allow_html=True)

        assigns = []
        for i in range(0, len(DEVELOPERS), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(DEVELOPERS):
                    dev = DEVELOPERS[i + j]
                    with col:
                        st.markdown(f"**{dev['name']}**")
                        c1, c2, c3 = st.columns(3)
                        with c1: pts = st.number_input("Pts", 0.0, step=0.5, key=f"sp_{dev['id']}")
                        with c2: pto = st.number_input("PTO", 0.0, 10.0, step=0.5, key=f"pto_a_{dev['id']}")
                        with c3:
                            teams = [t["name"] for t in TEAMS]
                            dt = team_assignments.get(dev["id"], "team1")
                            di = next((idx for idx, t in enumerate(TEAMS) if t["id"] == dt), 0)
                            tm = st.selectbox("Team", teams, di, key=f"tm_{dev['id']}")
                        if pts > 0:
                            tid = next(t["id"] for t in TEAMS if t["name"] == tm)
                            assigns.append({"engineerId": dev["id"], "teamId": tid, "storyPoints": pts, "totalPtoDays": pto})

        if st.form_submit_button("Save Sprint", type="primary", use_container_width=True):
            if not name: st.error("Enter sprint name")
            elif not assigns: st.error("Enter points for at least one developer")
            else:
                bd = sum(1 for d in range((end - start).days + 1) if (start + timedelta(days=d)).weekday() < 5)
                sprint = {
                    "sprintId": f"{start.year}-S{start.month:02d}-{start.day:02d}",
                    "sprintName": name,
                    "startDate": start.isoformat(),
                    "endDate": end.isoformat(),
                    "sprintDays": bd,
                    "assignments": assigns
                }
                if save_sprint(sprint):
                    st.success(f"'{name}' saved!")
                    st.balloons()

def render_team_analytics():
    sprints = load_sprints()
    if not sprints:
        st.info("No sprint data yet. Add your first sprint!")
        return

    recent = sprints[:6]
    def avg(tid): return sum(sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == tid) for s in recent) / len(recent) if recent else 0

    cols = st.columns(4)
    overall = sum(sum(a["storyPoints"] for a in s.get("assignments", [])) for s in recent) / len(recent) if recent else 0

    with cols[0]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Overall</div><div class="metric-value">{overall:.1f}</div><div class="metric-sub">pts/sprint</div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Team 1</div><div class="metric-value orange">{avg("team1"):.1f}</div><div class="metric-sub">pts/sprint</div></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Team 2</div><div class="metric-value green">{avg("team2"):.1f}</div><div class="metric-sub">pts/sprint</div></div>', unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Storyblok</div><div class="metric-value cyan">{avg("storyblok"):.1f}</div><div class="metric-sub">pts/sprint</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    data = [{"Sprint": s["sprintName"],
             "Team 1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
             "Team 2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
             "Storyblok": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")}
            for s in reversed(sprints[:12])]
    df = pd.DataFrame(data)

    fig = go.Figure()
    # Using sage green variations for chart differentiation
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 1"], mode="lines+markers", name="Team 1", line=dict(color="#4a5d4a", width=2), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 2"], mode="lines+markers", name="Team 2", line=dict(color="#6b8c6b", width=2), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Storyblok"], mode="lines+markers", name="Storyblok", line=dict(color="#8aaa8a", width=2, dash="dot"), marker=dict(size=6)))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafaf8", font=dict(color="#5a5a5a", size=11),
        height=300, margin=dict(t=40, b=60, l=50, r=20),
        xaxis=dict(gridcolor="#e5e5e0", linecolor="#e5e5e0", tickfont=dict(size=10, color="#6a6a6a"), tickangle=-45),
        yaxis=dict(gridcolor="#e5e5e0", linecolor="#e5e5e0", title=dict(text="Points", font=dict(color="#6a6a6a")), tickfont=dict(size=10, color="#6a6a6a")),
        legend=dict(orientation="h", y=1.25, x=0.5, xanchor="center", bgcolor="rgba(0,0,0,0)", font=dict(size=11, color="#5a5a5a")),
        hovermode="x unified"
    )
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    st.markdown('<p class="section-label">Recent Sprints</p>', unsafe_allow_html=True)
    tbl = [{"Sprint": s["sprintName"], "Period": f"{s['startDate']} → {s['endDate']}",
            "T1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
            "T2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
            "SB": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")}
           for s in sprints[:10]]
    st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

def render_individual():
    sprints = load_sprints()
    if not sprints:
        st.info("No sprint data yet.")
        return

    sel = st.selectbox("Select Developer", ["Select a developer..."] + [d["name"] for d in DEVELOPERS])
    if sel == "Select a developer...":
        st.markdown('<p style="color: #8a8a8a; font-size: 0.9rem;">Select a developer above to view their performance metrics.</p>', unsafe_allow_html=True)
        return

    dev = next((d for d in DEVELOPERS if d["name"] == sel), None)
    if not dev: return

    st.markdown("---")
    st.markdown(f"**{dev['name']}** · {dev['role']}")

    agg = {}
    for s in sprints:
        for a in s.get("assignments", []):
            if a["engineerId"] == dev["id"]:
                if s["sprintId"] not in agg:
                    agg[s["sprintId"]] = {"sprintId": s["sprintId"], "sprintName": s["sprintName"],
                                          "startDate": s["startDate"], "endDate": s["endDate"],
                                          "sprintDays": s["sprintDays"], "storyPoints": 0,
                                          "totalPtoDays": 0, "teams": []}
                agg[s["sprintId"]]["storyPoints"] += a["storyPoints"]
                agg[s["sprintId"]]["totalPtoDays"] = max(agg[s["sprintId"]]["totalPtoDays"], a.get("totalPtoDays", 0))
                agg[s["sprintId"]]["teams"].append(a["teamId"])

    data = sorted(agg.values(), key=lambda x: x["startDate"], reverse=True)
    vel = calculate_velocity(data)

    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Velocity</div><div class="metric-value green">{vel:.2f}</div><div class="metric-sub">pts/day</div></div>', unsafe_allow_html=True)
    with cols[1]:
        recent_pts = sum(d["storyPoints"] for d in data[:10])
        st.markdown(f'<div class="metric-card"><div class="metric-label">Recent Total</div><div class="metric-value">{recent_pts:.1f}</div><div class="metric-sub">last 10 sprints</div></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Sprints</div><div class="metric-value">{len(data)}</div><div class="metric-sub">tracked</div></div>', unsafe_allow_html=True)

    if data:
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        chart = [{"Sprint": d["sprintName"], "Velocity": d["storyPoints"] / (d["sprintDays"] - d["totalPtoDays"]) if d["sprintDays"] - d["totalPtoDays"] > 0 else 0} for d in reversed(data[:10])]
        df = pd.DataFrame(chart)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Velocity"], mode="lines+markers", line=dict(color="#5d6b5d", width=2), marker=dict(size=6), fill="tozeroy", fillcolor="rgba(93,107,93,0.1)"))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#fafaf8", font=dict(color="#5a5a5a", size=11),
            height=220, margin=dict(t=10, b=60, l=50, r=20), showlegend=False,
            xaxis=dict(gridcolor="#e5e5e0", linecolor="#e5e5e0", tickfont=dict(size=10, color="#6a6a6a"), tickangle=-45),
            yaxis=dict(gridcolor="#e5e5e0", linecolor="#e5e5e0", title=dict(text="pts/day", font=dict(color="#6a6a6a")), tickfont=dict(size=10, color="#6a6a6a"))
        )
        st.plotly_chart(fig, width='stretch')

        st.markdown("---")
        tbl = [{"Sprint": d["sprintName"], "Date": d["startDate"][:10], "Pts": d["storyPoints"], "PTO": d["totalPtoDays"],
                "Vel": f"{d['storyPoints']/(d['sprintDays']-d['totalPtoDays']):.2f}" if d["sprintDays"]-d["totalPtoDays"]>0 else "0"} for d in data[:15]]
        st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

# ============== MAIN ==============
def main():
    st.markdown('''
    <div class="app-header">
        <h1 class="app-title">✦ Sprint Velocity ✦</h1>
        <p class="app-subtitle">CHG Web Product Team</p>
    </div>
    ''', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["Forecast", "Add Sprint", "Team Analytics", "Individual"])
    with t1: render_forecast()
    with t2: render_add_sprint()
    with t3: render_team_analytics()
    with t4: render_individual()

if __name__ == "__main__":
    main()

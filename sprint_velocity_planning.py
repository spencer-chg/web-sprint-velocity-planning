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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============== SUPABASE CONNECTION ==============
SUPABASE_URL = "https://iwarvepodaijjofyyvvm.supabase.co"
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3YXJ2ZXBvZGFpampvZnl5dnZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzMDQyOTksImV4cCI6MjA4NTg4MDI5OX0.z9c_aYcY53G7Id3FSyNgrheNtKVWlSt5EGaoM-wAMWc"))

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# ============== CUSTOM CSS - POINTING POKER STYLE ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Base styling - warm cream background */
    .main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #f5f5f0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stSidebar"] {
        background: #eeeee8 !important;
    }

    /* Hide default elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #2d2d2d !important;
    }

    p, span, div, label {
        color: #4a4a4a;
    }

    /* Header styling */
    .app-header {
        text-align: center;
        padding: 48px 0 32px 0;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 600;
        color: #2d2d2d;
        letter-spacing: 0.02em;
        margin: 0;
    }

    .app-subtitle {
        color: #7a7a7a;
        font-size: 0.9rem;
        font-weight: 400;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.75rem;
    }

    /* Section headers with small caps */
    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #8a8a8a;
        margin-bottom: 16px;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #2d2d2d;
        margin: 0 0 8px 0;
    }

    /* Cards - clean, minimal */
    .card {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #e8e8e4;
    }

    .card-muted {
        background: #fafaf8;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
        border: 1px solid #eaeae6;
    }

    /* Team colors - muted palette */
    .team-orange { border-left: 3px solid #c4956a; }
    .team-green { border-left: 3px solid #6b7c6b; }
    .team-cyan { border-left: 3px solid #6b8a8a; }

    .color-orange { color: #c4956a; }
    .color-green { color: #6b7c6b; }
    .color-cyan { color: #6b8a8a; }

    /* Metric cards */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #e8e8e4;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.2;
        margin: 8px 0;
        color: #2d2d2d;
    }

    .metric-label {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #9a9a9a;
    }

    .metric-sublabel {
        font-size: 0.8rem;
        color: #7a7a7a;
        font-weight: 400;
    }

    /* Forecast cards */
    .forecast-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e8e8e4;
    }

    .forecast-team-name {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 4px;
    }

    .forecast-raw {
        color: #9a9a9a;
        font-size: 0.8rem;
        margin-bottom: 12px;
    }

    .forecast-value {
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }

    .forecast-buffer {
        color: #9a9a9a;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Breakdown items */
    .breakdown-item {
        background: #fafaf8;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #f0f0ec;
    }

    .breakdown-name {
        font-weight: 500;
        color: #3a3a3a;
        font-size: 0.9rem;
    }

    .breakdown-meta {
        color: #9a9a9a;
        font-size: 0.7rem;
        margin-top: 2px;
    }

    .breakdown-value {
        font-weight: 700;
        font-size: 1.1rem;
        color: #2d2d2d;
    }

    /* Tabs - minimal style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #e8e8e4;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 0;
        padding: 16px 32px;
        font-weight: 500;
        font-size: 0.85rem;
        color: #8a8a8a;
        border: none;
        border-bottom: 2px solid transparent;
        margin-bottom: -1px;
    }

    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #6b7c6b !important;
        border-bottom: 2px solid #6b7c6b !important;
    }

    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* Buttons - sage green */
    .stButton > button {
        background: #6b7c6b;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #5a6b5a;
        transform: translateY(-1px);
    }

    /* Form inputs - clean style */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        background: #ffffff !important;
        border: 1px solid #e0e0dc !important;
        border-radius: 8px !important;
        color: #2d2d2d !important;
        font-size: 0.9rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #6b7c6b !important;
        box-shadow: 0 0 0 1px #6b7c6b !important;
    }

    /* Select boxes */
    .stSelectbox > div > div {
        background: #ffffff !important;
    }

    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: #e0e0dc !important;
    }

    /* Number input */
    .stNumberInput > div {
        background: transparent !important;
    }

    /* Labels */
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stDateInput > label {
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: #8a8a8a !important;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #e8e8e4;
        margin: 32px 0;
    }

    /* Info boxes */
    .stAlert {
        background: #fafaf8 !important;
        border: 1px solid #e8e8e4 !important;
        border-radius: 8px !important;
        color: #5a5a5a !important;
    }

    /* Data table */
    .stDataFrame {
        border: 1px solid #e8e8e4;
        border-radius: 8px;
    }

    [data-testid="stDataFrame"] > div {
        background: #ffffff;
        border-radius: 8px;
    }

    /* Developer input card */
    .dev-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #e8e8e4;
    }

    .dev-name {
        font-weight: 600;
        color: #2d2d2d;
        font-size: 0.95rem;
        margin-bottom: 12px;
    }

    /* Team header card */
    .team-header {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #e8e8e4;
    }

    .team-name {
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
    }

    .team-meta {
        color: #9a9a9a;
        font-size: 0.8rem;
        margin-top: 4px;
    }

    .team-badge {
        background: #f5f5f0;
        padding: 4px 12px;
        border-radius: 20px;
        color: #7a7a7a;
        font-size: 0.7rem;
        font-weight: 500;
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

TEAM_COLORS = {"orange": "#c4956a", "green": "#6b7c6b", "cyan": "#6b8a8a"}

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
    """Load all sprints from Supabase"""
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
    """Save a new sprint to Supabase"""
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
    """Load current team assignments from Supabase"""
    try:
        result = supabase.table("team_assignments").select("*").execute()
        return {row["engineer_id"]: row["team_id"] for row in result.data}
    except:
        return {
            "fredrik-svensson": "team1", "fernando-fernandez": "team1",
            "matthew-callison": "team1", "cody-worthen": "team1",
            "stephen-corry": "team2", "tom-sharrock": "team2",
            "brady-hession": "team2", "jaime-virrueta": "team2"
        }

def update_team_assignment(engineer_id, team_id):
    """Update a developer's team assignment"""
    try:
        supabase.table("team_assignments").upsert({
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
    st.markdown('<p class="section-label">Planning</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Sprint Forecast</h2>', unsafe_allow_html=True)

    team_assignments = load_team_assignments()
    sprints = load_sprints()

    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        buffer_opts = {"70% (Conservative)": 0.70, "85% (Standard)": 0.85, "100% (Aggressive)": 1.00}
        sel = st.selectbox("Planning Buffer", list(buffer_opts.keys()), index=1)
        st.session_state.planning_buffer = buffer_opts[sel]
    with col3:
        calc = st.button("Calculate Forecast", type="primary", use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Team Assignments & PTO</p>', unsafe_allow_html=True)

    cols = st.columns(len(TEAMS))
    for idx, team in enumerate(TEAMS):
        with cols[idx]:
            color = TEAM_COLORS.get(team["color"], "#c4956a")
            devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team["id"]]

            st.markdown(f'''
            <div class="team-header team-{team['color']}">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <h4 class="team-name color-{team['color']}">{team['name']}</h4>
                        <p class="team-meta">{team['pmName']}</p>
                    </div>
                    <span class="team-badge">{len(devs)} devs</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            for dev in devs:
                st.markdown(f"**{dev['name']}**")
                c1, c2 = st.columns([3, 1])
                with c1:
                    pto = st.number_input("PTO days", 0.0, 10.0, st.session_state.pto_data.get(dev["id"], 0.0), 0.5, key=f"pto_{dev['id']}", label_visibility="collapsed")
                    st.session_state.pto_data[dev["id"]] = pto
                with c2:
                    others = [t for t in TEAMS if t["id"] != team["id"]]
                    mv = st.selectbox("Move", [""] + [t["name"] for t in others], key=f"mv_{dev['id']}", label_visibility="collapsed")
                    if mv:
                        new_team = next(t["id"] for t in others if t["name"] == mv)
                        update_team_assignment(dev["id"], new_team)
                        st.rerun()

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
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Results</p>', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">Forecast</h3>', unsafe_allow_html=True)

        f = st.session_state.forecast
        cols = st.columns(len(TEAMS))
        for idx, team in enumerate(TEAMS):
            r = f["teams"].get(team["id"], {})
            color = TEAM_COLORS.get(r.get("color", "orange"), "#c4956a")
            with cols[idx]:
                st.markdown(f'''
                <div class="forecast-card">
                    <div class="forecast-team-name color-{team['color']}">{r.get('name', team['name'])}</div>
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
    st.markdown('<p class="section-label">Data Entry</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Add Sprint Data</h2>', unsafe_allow_html=True)

    team_assignments = load_team_assignments()

    with st.form("add_sprint"):
        c1, c2, c3 = st.columns(3)
        with c1: name = st.text_input("Sprint Name", placeholder="e.g., Suttungr")
        with c2: start = st.date_input("Start Date")
        with c3: end = st.date_input("End Date", value=date.today() + timedelta(days=13))

        if start and end:
            hols = get_holidays_in_range(start, end)
            if hols: st.info(f"Holidays in this sprint: {', '.join(h['name'] for h in hols)}")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Developer Contributions</p>', unsafe_allow_html=True)

        assigns = []
        for i in range(0, len(DEVELOPERS), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(DEVELOPERS):
                    dev = DEVELOPERS[i + j]
                    with col:
                        st.markdown(f'<div class="dev-name">{dev["name"]}</div>', unsafe_allow_html=True)
                        c1, c2, c3 = st.columns(3)
                        with c1: pts = st.number_input("Points", 0.0, step=0.5, key=f"sp_{dev['id']}")
                        with c2: pto = st.number_input("PTO Days", 0.0, 10.0, step=0.5, key=f"pto_a_{dev['id']}")
                        with c3:
                            teams = [t["name"] for t in TEAMS]
                            dt = team_assignments.get(dev["id"], "team1")
                            di = next((idx for idx, t in enumerate(TEAMS) if t["id"] == dt), 0)
                            tm = st.selectbox("Team", teams, di, key=f"tm_{dev['id']}")
                        if pts > 0:
                            tid = next(t["id"] for t in TEAMS if t["name"] == tm)
                            assigns.append({"engineerId": dev["id"], "teamId": tid, "storyPoints": pts, "totalPtoDays": pto})
                        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        if st.form_submit_button("Save Sprint", type="primary", use_container_width=True):
            if not name: st.error("Please enter a sprint name")
            elif not assigns: st.error("Please enter points for at least one developer")
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
                    st.success(f"Sprint '{name}' saved successfully!")
                    st.balloons()

def render_team_analytics():
    st.markdown('<p class="section-label">Analytics</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Team Performance</h2>', unsafe_allow_html=True)

    sprints = load_sprints()
    if not sprints:
        st.info("No sprint data yet. Add your first sprint to see analytics.")
        return

    recent = sprints[:6]
    def avg(tid): return sum(sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == tid) for s in recent) / len(recent) if recent else 0

    c1, c2, c3, c4 = st.columns(4)
    overall = sum(sum(a["storyPoints"] for a in s.get("assignments", [])) for s in recent) / len(recent) if recent else 0

    with c1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Overall Average</div>
            <div class="metric-value">{overall:.1f}</div>
            <div class="metric-sublabel">points per sprint</div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
        <div class="metric-card team-orange">
            <div class="metric-label">Team 1</div>
            <div class="metric-value color-orange">{avg("team1"):.1f}</div>
            <div class="metric-sublabel">points per sprint</div>
        </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div class="metric-card team-green">
            <div class="metric-label">Team 2</div>
            <div class="metric-value color-green">{avg("team2"):.1f}</div>
            <div class="metric-sublabel">points per sprint</div>
        </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''
        <div class="metric-card team-cyan">
            <div class="metric-label">Storyblok</div>
            <div class="metric-value color-cyan">{avg("storyblok"):.1f}</div>
            <div class="metric-sublabel">points per sprint</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

    data = [{"Sprint": s["sprintName"],
             "Team 1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
             "Team 2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
             "Storyblok": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")}
            for s in reversed(sprints[:12])]
    df = pd.DataFrame(data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 1"], mode="lines+markers", name="Team 1",
                             line=dict(color="#c4956a", width=2), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 2"], mode="lines+markers", name="Team 2",
                             line=dict(color="#6b7c6b", width=2), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Storyblok"], mode="lines+markers", name="Storyblok",
                             line=dict(color="#6b8a8a", width=2), marker=dict(size=6)))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#fafaf8",
        font_color="#4a4a4a",
        height=320,
        xaxis=dict(gridcolor="#e8e8e4", linecolor="#e8e8e4"),
        yaxis=dict(gridcolor="#e8e8e4", linecolor="#e8e8e4", title="Story Points"),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
        margin=dict(t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">History</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Recent Sprints</h3>', unsafe_allow_html=True)

    tbl = [{"Sprint": s["sprintName"],
            "Period": f"{s['startDate']} → {s['endDate']}",
            "Team 1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
            "Team 2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
            "Storyblok": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")}
           for s in sprints[:10]]
    st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

def render_individual():
    st.markdown('<p class="section-label">Analytics</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Individual Performance</h2>', unsafe_allow_html=True)

    sprints = load_sprints()
    if not sprints:
        st.info("No sprint data yet.")
        return

    sel = st.selectbox("Select Developer", ["Choose a developer..."] + [d["name"] for d in DEVELOPERS])
    if sel == "Choose a developer...":
        st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
        st.markdown("Select a developer above to view their performance metrics.")
        return

    dev = next((d for d in DEVELOPERS if d["name"] == sel), None)
    if not dev: return

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<h3 class="section-title">{dev["name"]}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#7a7a7a;margin-top:-8px;">{dev["role"]}</p>', unsafe_allow_html=True)

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

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'''
        <div class="metric-card team-green">
            <div class="metric-label">Velocity</div>
            <div class="metric-value color-green">{vel:.2f}</div>
            <div class="metric-sublabel">points per day</div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Total Points</div>
            <div class="metric-value">{sum(d["storyPoints"] for d in data):.1f}</div>
            <div class="metric-sublabel">all time</div>
        </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Sprints</div>
            <div class="metric-value">{len(data)}</div>
            <div class="metric-sublabel">tracked</div>
        </div>
        ''', unsafe_allow_html=True)

    if data:
        st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

        chart = [{"Sprint": d["sprintName"],
                  "Velocity": d["storyPoints"] / (d["sprintDays"] - d["totalPtoDays"]) if d["sprintDays"] - d["totalPtoDays"] > 0 else 0}
                 for d in reversed(data[:10])]
        df = pd.DataFrame(chart)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Velocity"], mode="lines+markers",
                                 line=dict(color="#6b7c6b", width=2), marker=dict(size=8),
                                 fill="tozeroy", fillcolor="rgba(107,124,107,0.1)"))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#fafaf8",
            font_color="#4a4a4a",
            height=260,
            xaxis=dict(gridcolor="#e8e8e4", linecolor="#e8e8e4"),
            yaxis=dict(gridcolor="#e8e8e4", linecolor="#e8e8e4", title="Points per Day"),
            showlegend=False,
            margin=dict(t=20, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">History</p>', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">Sprint History</h3>', unsafe_allow_html=True)

        tbl = [{"Sprint": d["sprintName"],
                "Date": d["startDate"][:10],
                "Teams": ", ".join(set("T1" if t=="team1" else "T2" if t=="team2" else "SB" for t in d["teams"])),
                "Points": d["storyPoints"],
                "PTO": d["totalPtoDays"],
                "Velocity": f"{d['storyPoints']/(d['sprintDays']-d['totalPtoDays']):.2f}" if d["sprintDays"]-d["totalPtoDays"]>0 else "0"}
               for d in data[:15]]
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

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

# ============== DESIGN SYSTEM ==============
# Colors
CREAM = "#f5f5f0"
CREAM_LIGHT = "#faf9f6"
SAGE = "#6b7c6b"
SAGE_DARK = "#5a6a5a"
SAGE_DARKER = "#4a5a4a"
TEXT_PRIMARY = "#4a4a4a"
TEXT_SECONDARY = "#7a7a7a"
TEXT_MUTED = "#9a9a9a"
BORDER = "#e5e5e0"
BORDER_LIGHT = "#eeeeea"

# ============== CUSTOM CSS ==============
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ===== BASE ===== */
    :root {{
        --sage: {SAGE};
        --cream: {CREAM};
    }}

    html, body, .main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: {CREAM} !important;
    }}

    .stApp > header {{ background: transparent !important; }}

    #MainMenu, footer, header, .stDeployButton, [data-testid="stDecoration"] {{
        display: none !important;
    }}

    .block-container {{
        max-width: 960px !important;
        padding: 2rem 1rem 4rem 1rem !important;
    }}

    * {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }}

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4, h5, h6 {{ color: {TEXT_PRIMARY} !important; }}
    p, span, div {{ color: {TEXT_PRIMARY} !important; }}
    strong, b {{ color: {TEXT_PRIMARY} !important; }}

    /* ===== HEADER ===== */
    .app-header {{
        text-align: center;
        padding: 32px 0 24px 0;
    }}
    .app-title {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin: 0;
    }}
    .app-subtitle {{
        color: {TEXT_MUTED};
        font-size: 0.85rem;
        margin-top: 8px;
    }}

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0;
        background: transparent !important;
        border-bottom: 1px solid {BORDER};
        justify-content: center;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        color: {TEXT_SECONDARY} !important;
        border-bottom: 2px solid transparent !important;
        margin-bottom: -1px;
    }}
    .stTabs [aria-selected="true"] {{
        color: {SAGE} !important;
        border-bottom: 2px solid {SAGE} !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{ color: {SAGE} !important; }}
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none !important; }}

    /* ===== TEAM CARD ===== */
    .team-card {{
        background: {CREAM_LIGHT};
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid {BORDER};
        border-left: 4px solid {SAGE};
    }}
    .team-name {{
        font-size: 1rem;
        font-weight: 600;
        color: {TEXT_PRIMARY};
        margin: 0 0 4px 0;
    }}
    .team-meta {{
        font-size: 0.75rem;
        color: {TEXT_SECONDARY};
    }}

    /* ===== DEVELOPER ROW ===== */
    .dev-row {{
        background: {CREAM_LIGHT};
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 10px;
        border: 1px solid {BORDER_LIGHT};
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }}
    .dev-name {{
        font-size: 0.9rem;
        font-weight: 500;
        color: {TEXT_PRIMARY};
        flex: 1;
    }}
    .dev-pto {{
        display: flex;
        align-items: center;
        gap: 0;
    }}
    .pto-value {{
        background: white;
        border-top: 1px solid {BORDER};
        border-bottom: 1px solid {BORDER};
        padding: 8px 16px;
        min-width: 50px;
        text-align: center;
        font-weight: 500;
        font-size: 0.9rem;
        color: {TEXT_PRIMARY};
    }}

    /* ===== PTO BUTTONS (custom) ===== */
    .pto-btn {{
        background: {SAGE} !important;
        color: white !important;
        border: none !important;
        width: 40px !important;
        height: 40px !important;
        font-size: 1.25rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: background 0.15s !important;
    }}
    .pto-btn:hover {{
        background: {SAGE_DARK} !important;
    }}
    .pto-btn-minus {{
        border-radius: 8px 0 0 8px !important;
    }}
    .pto-btn-plus {{
        border-radius: 0 8px 8px 0 !important;
    }}

    /* ===== MAIN BUTTONS ===== */
    .stButton > button {{
        background: {SAGE} !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}
    .stButton > button:hover {{
        background: {SAGE_DARK} !important;
    }}

    /* Small buttons for +/- */
    div[data-testid="column"] .stButton > button {{
        padding: 0 !important;
        min-height: 40px !important;
        width: 40px !important;
        font-size: 1.25rem !important;
    }}

    /* ===== SELECT BOXES ===== */
    .stSelectbox [data-baseweb="select"] {{
        background: {CREAM_LIGHT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
    }}
    .stSelectbox [data-baseweb="select"] > div {{
        background: {CREAM_LIGHT} !important;
        color: {TEXT_PRIMARY} !important;
    }}
    .stSelectbox [data-baseweb="select"]:focus-within {{
        border-color: {SAGE} !important;
        box-shadow: 0 0 0 1px {SAGE} !important;
    }}

    /* ===== DROPDOWN MENUS ===== */
    [data-baseweb="popover"], [data-baseweb="menu"] {{
        background: {CREAM_LIGHT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
    }}
    [data-baseweb="menu"] li, [role="option"] {{
        background: {CREAM_LIGHT} !important;
        color: {TEXT_PRIMARY} !important;
    }}
    [data-baseweb="menu"] li:hover, [role="option"]:hover {{
        background: {BORDER_LIGHT} !important;
    }}

    /* ===== METRIC CARDS ===== */
    .metric-card {{
        background: {CREAM_LIGHT};
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid {BORDER};
    }}
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {SAGE};
    }}
    .metric-label {{
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {TEXT_SECONDARY};
        margin-bottom: 4px;
    }}

    /* ===== FORECAST RESULTS ===== */
    .forecast-card {{
        background: {CREAM_LIGHT};
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        border: 1px solid {BORDER};
    }}
    .forecast-team {{
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {SAGE};
        margin-bottom: 8px;
    }}
    .forecast-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {SAGE};
    }}
    .forecast-sub {{
        font-size: 0.8rem;
        color: {TEXT_SECONDARY};
        margin-top: 4px;
    }}

    /* ===== BREAKDOWN ===== */
    .breakdown-item {{
        background: {CREAM};
        border-radius: 8px;
        padding: 10px 12px;
        margin-top: 8px;
        display: flex;
        justify-content: space-between;
    }}
    .breakdown-name {{
        font-size: 0.85rem;
        color: {TEXT_PRIMARY};
    }}
    .breakdown-value {{
        font-weight: 600;
        color: {TEXT_PRIMARY};
    }}

    /* ===== DIVIDER ===== */
    hr {{
        border: none;
        height: 1px;
        background: {BORDER};
        margin: 20px 0;
    }}

    /* ===== DATA TABLES ===== */
    .stDataFrame {{ border-radius: 8px; }}

    /* ===== HIDE NUMBER INPUT DEFAULTS ===== */
    .stNumberInput {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# ============== DATA ==============
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
    {"id": "team1", "name": "Team 1", "displayName": "Web Team 1", "pmName": "Jason and Spencer"},
    {"id": "team2", "name": "Team 2", "displayName": "Web Team 2", "pmName": "Matt and Matt"},
    {"id": "storyblok", "name": "Storyblok", "displayName": "Storyblok Team", "pmName": "Storyblok"},
]

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
    return {
        "fredrik-svensson": "team1", "fernando-fernandez": "team1",
        "matthew-callison": "team1", "cody-worthen": "team1",
        "stephen-corry": "team2", "tom-sharrock": "team2",
        "brady-hession": "team2", "jaime-virrueta": "team2"
    }

def update_team_assignment(engineer_id, team_id):
    try:
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

# ============== CUSTOM COMPONENTS ==============
def pto_stepper(dev_id, dev_name):
    """Custom PTO stepper with styled +/- buttons"""
    key_base = f"pto_{dev_id}"
    current = st.session_state.pto_data.get(dev_id, 0.0)

    col1, col2, col3, col4 = st.columns([3, 1, 1.2, 1])

    with col1:
        st.markdown(f"<div style='padding:8px 0; font-weight:500;'>{dev_name}</div>", unsafe_allow_html=True)

    with col2:
        if st.button("−", key=f"{key_base}_minus", use_container_width=True):
            st.session_state.pto_data[dev_id] = max(0.0, current - 0.5)
            st.rerun()

    with col3:
        st.markdown(f"""
        <div style='background:white; border:1px solid {BORDER}; border-radius:0;
                    padding:8px 0; text-align:center; font-weight:500; height:40px;
                    display:flex; align-items:center; justify-content:center;'>
            {current:.1f}
        </div>
        """, unsafe_allow_html=True)

    with col4:
        if st.button("+", key=f"{key_base}_plus", use_container_width=True):
            st.session_state.pto_data[dev_id] = min(10.0, current + 0.5)
            st.rerun()

def move_dropdown(dev_id, current_team_id):
    """Compact move dropdown"""
    other_teams = [t for t in TEAMS if t["id"] != current_team_id]
    options = ["Move..."] + [t["name"] for t in other_teams]
    selected = st.selectbox("", options, key=f"mv_{dev_id}", label_visibility="collapsed")
    if selected != "Move...":
        new_team_id = next(t["id"] for t in other_teams if t["name"] == selected)
        update_team_assignment(dev_id, new_team_id)
        st.rerun()

# ============== VIEWS ==============
def render_forecast():
    team_assignments = load_team_assignments()
    sprints = load_sprints()

    # Buffer + Calculate
    col1, col2 = st.columns([3, 1])
    with col1:
        buffer_opts = {"85% (Standard)": 0.85, "70% (Conservative)": 0.70, "100% (Aggressive)": 1.00}
        sel = st.selectbox("Planning Buffer", list(buffer_opts.keys()), index=0)
        st.session_state.planning_buffer = buffer_opts[sel]
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        calc = st.button("Calculate", type="primary", use_container_width=True)

    st.markdown("---")

    # 3-column team layout
    cols = st.columns(3)

    for idx, team in enumerate(TEAMS):
        with cols[idx]:
            devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team["id"]]

            # Team card
            st.markdown(f"""
            <div class="team-card">
                <div class="team-name">{team['name']}</div>
                <div class="team-meta">{team['pmName']} · {len(devs)} devs</div>
            </div>
            """, unsafe_allow_html=True)

            if devs:
                for dev in devs:
                    pto_stepper(dev["id"], dev["name"])
                    move_dropdown(dev["id"], team["id"])
                    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color:{TEXT_MUTED}; font-style:italic;'>No developers</p>", unsafe_allow_html=True)

    # Calculate forecast
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
            results[team["id"]] = {"name": team["displayName"], "assigns": assigns,
                                   "raw": sum(a["raw"] for a in assigns), "buf": round_to_half(sum(a["buf"] for a in assigns))}
        st.session_state.forecast = {"buffer": buf, "teams": results}

    # Display forecast results
    if st.session_state.forecast:
        st.markdown("---")
        st.markdown(f"<p style='font-size:0.7rem; font-weight:500; text-transform:uppercase; letter-spacing:0.05em; color:{TEXT_SECONDARY};'>Forecast Results</p>", unsafe_allow_html=True)

        f = st.session_state.forecast
        cols = st.columns(3)
        for idx, team in enumerate(TEAMS):
            r = f["teams"].get(team["id"], {})
            with cols[idx]:
                st.markdown(f"""
                <div class="forecast-card">
                    <div class="forecast-team">{r.get('name', team['name'])}</div>
                    <div class="forecast-value">{r.get('buf', 0):.1f}</div>
                    <div class="forecast-sub">Raw: {r.get('raw', 0):.1f} · {int(f['buffer']*100)}% buffer</div>
                </div>
                """, unsafe_allow_html=True)

                for a in r.get("assigns", []):
                    st.markdown(f"""
                    <div class="breakdown-item">
                        <span class="breakdown-name">{a['name']}</span>
                        <span class="breakdown-value">{a['buf']:.1f}</span>
                    </div>
                    """, unsafe_allow_html=True)

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
        st.markdown(f"<p style='font-size:0.7rem; font-weight:500; text-transform:uppercase; color:{TEXT_SECONDARY};'>Developer Points</p>", unsafe_allow_html=True)

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
        st.markdown(f'<div class="metric-card"><div class="metric-label">Overall</div><div class="metric-value">{overall:.1f}</div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Team 1</div><div class="metric-value">{avg("team1"):.1f}</div></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Team 2</div><div class="metric-value">{avg("team2"):.1f}</div></div>', unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Storyblok</div><div class="metric-value">{avg("storyblok"):.1f}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Chart
    data = [{"Sprint": s["sprintName"],
             "Team 1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
             "Team 2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
             "Storyblok": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")}
            for s in reversed(sprints[:12])]
    df = pd.DataFrame(data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 1"], mode="lines+markers", name="Team 1", line=dict(color=SAGE, width=2)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 2"], mode="lines+markers", name="Team 2", line=dict(color=SAGE_DARK, width=2)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Storyblok"], mode="lines+markers", name="Storyblok", line=dict(color=TEXT_SECONDARY, width=2, dash="dot")))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=CREAM_LIGHT,
        font=dict(color=TEXT_PRIMARY, size=11), height=300,
        margin=dict(t=40, b=60, l=50, r=20),
        xaxis=dict(gridcolor=BORDER, tickangle=-45),
        yaxis=dict(gridcolor=BORDER, title="Points"),
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown(f"<p style='font-size:0.7rem; font-weight:500; text-transform:uppercase; color:{TEXT_SECONDARY};'>Recent Sprints</p>", unsafe_allow_html=True)
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

    sel = st.selectbox("Select Developer", ["Select..."] + [d["name"] for d in DEVELOPERS])
    if sel == "Select...":
        st.markdown(f"<p style='color:{TEXT_MUTED};'>Select a developer to view their metrics.</p>", unsafe_allow_html=True)
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
                                          "sprintDays": s["sprintDays"], "storyPoints": 0, "totalPtoDays": 0}
                agg[s["sprintId"]]["storyPoints"] += a["storyPoints"]
                agg[s["sprintId"]]["totalPtoDays"] = max(agg[s["sprintId"]]["totalPtoDays"], a.get("totalPtoDays", 0))

    data = sorted(agg.values(), key=lambda x: x["startDate"], reverse=True)
    vel = calculate_velocity(data)

    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Velocity</div><div class="metric-value">{vel:.2f}</div></div>', unsafe_allow_html=True)
    with cols[1]:
        recent_pts = sum(d["storyPoints"] for d in data[:10])
        st.markdown(f'<div class="metric-card"><div class="metric-label">Last 10</div><div class="metric-value">{recent_pts:.1f}</div></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Sprints</div><div class="metric-value">{len(data)}</div></div>', unsafe_allow_html=True)

    if data:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        chart = [{"Sprint": d["sprintName"], "Velocity": d["storyPoints"] / (d["sprintDays"] - d["totalPtoDays"]) if d["sprintDays"] - d["totalPtoDays"] > 0 else 0} for d in reversed(data[:10])]
        df = pd.DataFrame(chart)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Velocity"], mode="lines+markers", line=dict(color=SAGE, width=2), fill="tozeroy", fillcolor=f"rgba(107,124,107,0.1)"))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=CREAM_LIGHT,
            font=dict(color=TEXT_PRIMARY), height=220, margin=dict(t=10, b=60, l=50, r=20),
            showlegend=False, xaxis=dict(gridcolor=BORDER, tickangle=-45), yaxis=dict(gridcolor=BORDER, title="pts/day")
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        tbl = [{"Sprint": d["sprintName"], "Date": d["startDate"][:10], "Pts": d["storyPoints"], "PTO": d["totalPtoDays"]} for d in data[:15]]
        st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

# ============== MAIN ==============
def main():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">✦ Sprint Velocity ✦</h1>
        <p class="app-subtitle">CHG Web Product Team</p>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["Forecast", "Add Sprint", "Team Analytics", "Individual"])
    with t1: render_forecast()
    with t2: render_add_sprint()
    with t3: render_team_analytics()
    with t4: render_individual()

if __name__ == "__main__":
    main()

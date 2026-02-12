"""
Sprint Velocity Planning - Streamlit App
CHG Web Product Team
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from supabase import create_client
import os

# ============== CONFIG ==============
st.set_page_config(page_title="Sprint Velocity", page_icon="✦", layout="centered")

SUPABASE_URL = "https://iwarvepodaijjofyyvvm.supabase.co"
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3YXJ2ZXBvZGFpampvZnl5dnZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzMDQyOTksImV4cCI6MjA4NTg4MDI5OX0.z9c_aYcY53G7Id3FSyNgrheNtKVWlSt5EGaoM-wAMWc"))

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# ============== BEAUTIFUL CSS ==============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* === BASE === */
:root { --sage: #6b7c6b; --sage-dark: #5a6a5a; --cream: #f5f5f0; --text: #3a3a3a; --text-muted: #888; }
html, body, .stApp, [data-testid="stAppViewContainer"] { background: var(--cream) !important; }
.stApp > header { background: transparent !important; }
#MainMenu, footer, .stDeployButton { display: none !important; }
* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
.block-container { max-width: 900px !important; padding: 1.5rem 2rem 4rem !important; }

/* === HEADER === */
.header { text-align: center; padding: 24px 0 20px; }
.header h1 { font-size: 1.5rem; font-weight: 700; color: var(--text); margin: 0; letter-spacing: -0.02em; }
.header p { font-size: 0.75rem; color: var(--text-muted); margin: 6px 0 0; letter-spacing: 0.02em; }

/* === TABS === */
.stTabs [data-baseweb="tab-list"] { justify-content: center; border-bottom: 1px solid #e8e8e3; gap: 0; background: transparent; }
.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 12px 24px !important;
    transition: color 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--sage) !important; }
.stTabs [aria-selected="true"] { color: var(--sage) !important; border-bottom: 2px solid var(--sage) !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* === TEAM HEADER === */
.team-header {
    text-align: center;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
    padding: 8px 0 12px;
}

.forecast-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.forecast-card .label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; color: #aaa; margin-bottom: 4px; }
.forecast-card .value { font-size: 2.25rem; font-weight: 700; color: var(--sage); line-height: 1.1; }
.forecast-card .sub { font-size: 0.7rem; color: #bbb; margin-top: 4px; }

.metric {
    background: white;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.metric .label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.06em; color: #aaa; margin-bottom: 2px; }
.metric .value { font-size: 1.75rem; font-weight: 700; color: var(--sage); }

/* === BUTTONS === */
.stButton button {
    background: var(--sage) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 20px !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 2px 4px rgba(107,124,107,0.2) !important;
}
.stButton button:hover {
    background: var(--sage-dark) !important;
    box-shadow: 0 4px 8px rgba(107,124,107,0.25) !important;
}
.stButton button, .stSelectbox, .stNumberInput { white-space: nowrap !important; min-width: fit-content !important; }

/* Number inputs */
.stNumberInput input {
    text-align: center !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Tighter vertical spacing */
.stSelectbox, .stButton { margin-bottom: -10px !important; }

/* === FORM INPUTS === */
.stTextInput input, .stDateInput input {
    background: white !important;
    border: 1px solid #e5e5e0 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput input:focus, .stDateInput input:focus {
    border-color: var(--sage) !important;
    box-shadow: 0 0 0 3px rgba(107,124,107,0.1) !important;
}
.stSelectbox > div > div {
    background: white !important;
    border: 1px solid #e5e5e0 !important;
    border-radius: 10px !important;
    transition: border-color 0.2s ease !important;
}
.stSelectbox > div > div:hover { border-color: #ccc !important; }

/* Dropdown menu styling */
[data-baseweb="popover"] { border-radius: 12px !important; box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important; }
[data-baseweb="menu"] { border-radius: 12px !important; }
[data-baseweb="menu"] li { padding: 10px 16px !important; font-size: 0.9rem !important; transition: background 0.15s ease !important; }
[data-baseweb="menu"] li:hover { background: var(--cream) !important; }
[data-baseweb="menu"] li[aria-selected="true"] { background: rgba(107,124,107,0.1) !important; }

/* === DATA TABLES === */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
.stDataFrame [data-testid="stDataFrameResizable"] { border: 1px solid #e8e8e3 !important; border-radius: 12px !important; }
[data-testid="stDataFrame"] thead th {
    background: #fafaf8 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
}
[data-testid="stDataFrame"] tbody td { font-size: 0.85rem !important; }

/* === LAYOUT === */
[data-testid="stHorizontalBlock"] { gap: 8px !important; align-items: center !important; }
[data-testid="column"] { padding: 0 !important; margin: 0 !important; }

/* === SECTION HEADERS === */
.section-header {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    margin: 8px 0 20px;
    letter-spacing: -0.01em;
}

/* === MISC === */
hr { border: none; height: 1px; background: linear-gradient(to right, transparent, #e0e0db, transparent); margin: 28px 0; }

/* Hide anchor/jump links on headings */
h1 a, h2 a, h3 a, h4 a { display: none !important; }

/* Info box styling */
.stAlert { border-radius: 12px !important; border: none !important; }
[data-baseweb="notification"] { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ============== DATA ==============
DEVELOPERS = [
    {"id": "brady-hession", "name": "Brady Hession"},
    {"id": "cody-worthen", "name": "Cody Worthen"},
    {"id": "fernando-fernandez", "name": "Fernando Fernandez"},
    {"id": "fredrik-svensson", "name": "Fredrik Svensson"},
    {"id": "jaime-virrueta", "name": "Jaime Virrueta"},
    {"id": "matthew-callison", "name": "Matthew Callison"},
    {"id": "stephen-corry", "name": "Stephen Corry"},
    {"id": "tom-sharrock", "name": "Tom Sharrock"},
]

# Active teams (for forecasting and new sprints)
TEAMS = [
    {"id": "team1", "name": "Team 1", "pm": "Jason & Spencer"},
    {"id": "team2", "name": "Team 2", "pm": "Matt & Matt"},
]

# All teams including legacy (for historical data)
ALL_TEAMS = TEAMS + [{"id": "storyblok", "name": "Storyblok", "pm": "Storyblok"}]

HOLIDAYS = [
    {"name": "New Year's Day", "month": 1, "day": 1, "type": "full"},
    {"name": "MLK Day", "month": 1, "pattern": "third-monday", "type": "full"},
    {"name": "Memorial Day", "month": 5, "pattern": "last-monday", "type": "full"},
    {"name": "Independence Day", "month": 7, "day": 4, "type": "full"},
    {"name": "Labor Day", "month": 9, "pattern": "first-monday", "type": "full"},
    {"name": "Thanksgiving", "month": 11, "pattern": "fourth-thursday", "type": "full"},
    {"name": "Day after Thanksgiving", "month": 11, "pattern": "fourth-friday", "type": "full"},
    {"name": "Christmas Eve", "month": 12, "day": 24, "type": "half"},
    {"name": "Christmas Day", "month": 12, "day": 25, "type": "full"},
    {"name": "New Year's Eve", "month": 12, "day": 31, "type": "half"},
]

# ============== DB FUNCTIONS ==============
def load_sprints():
    try:
        result = supabase.table("sprints").select("*").order("start_date", desc=True).execute()
        sprints = []
        for s in result.data:
            assignments = supabase.table("sprint_assignments").select("*").eq("sprint_id", s["sprint_id"]).execute()
            sprints.append({
                "sprintId": s["sprint_id"], "sprintName": s["sprint_name"],
                "startDate": s["start_date"], "endDate": s["end_date"], "sprintDays": s["sprint_days"],
                "assignments": [{"engineerId": a["engineer_id"], "teamId": a["team_id"],
                                 "storyPoints": float(a["story_points"]), "totalPtoDays": float(a["pto_days"])} for a in assignments.data]
            })
        return sprints
    except: return []

def save_sprint(data):
    try:
        # Check if a sprint with this name already exists
        existing = supabase.table("sprints").select("*").eq("sprint_name", data["sprintName"]).execute()

        if existing.data:
            # Sprint exists — use its existing sprint_id
            sprint_id = existing.data[0]["sprint_id"]
        else:
            # New sprint — insert it
            sprint_id = data["sprintId"]
            supabase.table("sprints").insert({"sprint_id": sprint_id, "sprint_name": data["sprintName"],
                "start_date": data["startDate"], "end_date": data["endDate"], "sprint_days": data["sprintDays"]}).execute()

        # Upsert assignments: update if engineer already has a record, otherwise insert
        for a in data["assignments"]:
            existing_assign = supabase.table("sprint_assignments").select("*").eq(
                "sprint_id", sprint_id).eq("engineer_id", a["engineerId"]).eq("team_id", a["teamId"]).execute()

            if existing_assign.data:
                # Update existing assignment
                supabase.table("sprint_assignments").update({
                    "story_points": a["storyPoints"], "pto_days": a["totalPtoDays"]
                }).eq("id", existing_assign.data[0]["id"]).execute()
            else:
                # Insert new assignment
                supabase.table("sprint_assignments").insert({"sprint_id": sprint_id, "engineer_id": a["engineerId"],
                    "team_id": a["teamId"], "story_points": a["storyPoints"], "pto_days": a["totalPtoDays"]}).execute()
        return True
    except: return False

def load_team_assignments():
    try:
        result = supabase.table("team_assignments").select("*").execute()
        if result.data: return {r["engineer_id"]: r["team_id"] for r in result.data}
    except: pass
    # Default assignments - all devs on Team 1 or Team 2
    return {"fredrik-svensson": "team1", "fernando-fernandez": "team1", "matthew-callison": "team1", "cody-worthen": "team1",
            "stephen-corry": "team2", "tom-sharrock": "team2", "brady-hession": "team2", "jaime-virrueta": "team2"}

def save_team_assignment(eng_id, team_id):
    try:
        supabase.table("team_assignments").delete().eq("engineer_id", eng_id).execute()
        supabase.table("team_assignments").insert({"engineer_id": eng_id, "team_id": team_id}).execute()
        # Invalidate cache so next load gets fresh data
        st.session_state.team_assignments = None
    except: pass

# ============== UTILS ==============
def calc_holiday_date(year, month, pattern):
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

def get_holidays(start, end):
    if isinstance(start, str): start = datetime.strptime(start, "%Y-%m-%d").date()
    if isinstance(end, str): end = datetime.strptime(end, "%Y-%m-%d").date()
    result = []
    for h in HOLIDAYS:
        hd = date(start.year, h["month"], h["day"]) if h.get("day") else calc_holiday_date(start.year, h["month"], h.get("pattern"))
        if hd and start <= hd <= end: result.append(h)
    return result

def round_half(n): return round(n * 2) / 2

def calc_velocity(assignments, lookback=10):
    valid = [a for a in assignments if a.get("storyPoints", 0) > 0]
    if not valid: return 0
    weights = {"recent": 0.50, "mid": 0.30, "older": 0.15, "oldest": 0.05}
    tv, tw = 0, 0
    for i, a in enumerate(valid[:lookback]):
        hd = sum(1 if h["type"] == "full" else 0.5 for h in get_holidays(a.get("startDate", ""), a.get("endDate", ""))) if a.get("startDate") else 0
        wd = a.get("sprintDays", 10) - a.get("totalPtoDays", 0) - hd
        v = a["storyPoints"] / wd if wd > 0 else 0
        n = i + 1
        w = weights["recent"]/3 if n <= 3 else weights["mid"]/3 if n <= 6 else weights["older"]/3 if n <= 9 else weights["oldest"]/(lookback-9) if lookback > 9 else 0
        tv += v * w
        tw += w
    return tv / tw if tw > 0 else 0

# ============== STATE ==============
if "pto" not in st.session_state: st.session_state.pto = {}
if "forecast" not in st.session_state: st.session_state.forecast = None
if "buffer" not in st.session_state: st.session_state.buffer = 0.85
if "team_assignments" not in st.session_state: st.session_state.team_assignments = None
if "sprints_cache" not in st.session_state: st.session_state.sprints_cache = None

def get_team_assignments(force_refresh=False):
    """Get team assignments from cache or DB"""
    if force_refresh or st.session_state.team_assignments is None:
        st.session_state.team_assignments = load_team_assignments()
    return st.session_state.team_assignments

def get_sprints(force_refresh=False):
    """Get sprints from cache or DB"""
    if force_refresh or st.session_state.sprints_cache is None:
        st.session_state.sprints_cache = load_sprints()
    return st.session_state.sprints_cache

# ============== COMPONENTS ==============
def render_dev_row(dev):
    """Developer row: [Name] [number input with +/-]"""
    dev_id = dev["id"]
    first = dev["name"].split()[0]
    pto = st.session_state.pto.get(dev_id, 0.0)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"**{first}**")
    with c2:
        new_val = st.number_input(
            "PTO", value=pto, min_value=0.0, max_value=10.0, step=0.5,
            format="%.1f", key=f"pto_{dev_id}", label_visibility="collapsed"
        )
        if new_val != pto:
            st.session_state.pto[dev_id] = new_val
            st.rerun()

# ============== PAGES ==============
def page_forecast():
    # Use cached data - no DB calls on +/- clicks
    team_assignments = get_team_assignments()

    # Buffer selector + Calculate button - centered, compact
    _, c1, gap, c2, _ = st.columns([1, 1, 0.2, 0.8, 1])
    with c1:
        st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
        buf_val = st.select_slider(
            "Buffer",
            options=["70%", "85%", "100%"],
            value="85%",
            label_visibility="collapsed"
        )
        st.session_state.buffer = {"70%": 0.70, "85%": 0.85, "100%": 1.0}[buf_val]
    with c2:
        calc_btn = st.button("Calculate", type="primary", use_container_width=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Team headers - 2 columns with spacer
    card_cols = st.columns([1, 0.15, 1])
    for i, team in enumerate(TEAMS):
        with card_cols[i * 2]:
            st.markdown(f"<div class='team-header'>{team['name']}</div>", unsafe_allow_html=True)

    # Column headers for PTO
    hdr_cols = st.columns([1, 0.15, 1])
    for i, team in enumerate(TEAMS):
        with hdr_cols[i * 2]:
            h1, h2 = st.columns([2, 1])
            with h2:
                st.markdown("<div style='font-size:0.7rem; color:#aaa; text-transform:uppercase; letter-spacing:0.05em; text-align:center;'>PTO Days</div>", unsafe_allow_html=True)

    # Developer rows - 2 columns with spacer
    dev_cols = st.columns([1, 0.15, 1])
    for i, team in enumerate(TEAMS):
        with dev_cols[i * 2]:  # 0 and 2 (skip spacer at 1)
            devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team["id"]]
            if devs:
                for dev in devs:
                    render_dev_row(dev)
            else:
                st.markdown("<p style='color:#999; font-size:0.85rem; text-align:center; margin-top:8px;'>No developers</p>", unsafe_allow_html=True)

    # Calculate - only load sprints from DB when button is clicked
    if calc_btn:
        sprints = get_sprints(force_refresh=True)  # Fresh data on Calculate
        team_assignments = get_team_assignments(force_refresh=True)
        buf = st.session_state.buffer
        results = {}
        for team in TEAMS:
            devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team["id"]]
            assigns = []
            for dev in devs:
                dev_sprints = [{**a, "sprintDays": s["sprintDays"], "startDate": s["startDate"], "endDate": s["endDate"]}
                              for s in sprints for a in s.get("assignments", []) if a["engineerId"] == dev["id"]]
                vel = calc_velocity(dev_sprints)
                pto = st.session_state.pto.get(dev["id"], 0)
                raw = vel * (10 - pto)
                assigns.append({"name": dev["name"].split()[0], "raw": raw, "buf": round_half(raw * buf)})
            results[team["id"]] = {"name": team["name"], "assigns": assigns,
                                   "raw": sum(a["raw"] for a in assigns), "buf": round_half(sum(a["buf"] for a in assigns))}
        st.session_state.forecast = {"buffer": buf, "teams": results}

    # Show forecast
    if st.session_state.forecast:
        st.markdown("---")
        f = st.session_state.forecast
        cols = st.columns([1, 0.15, 1])
        for i, team in enumerate(TEAMS):
            r = f["teams"].get(team["id"], {})
            with cols[i * 2]:  # 0 and 2 (skip spacer)
                st.markdown(f"""
                <div class="forecast-card">
                    <div class="label">{team['name']}</div>
                    <div class="value">{r.get('buf', 0):.1f}</div>
                    <div class="sub">Raw: {r.get('raw', 0):.1f}</div>
                </div>
                """, unsafe_allow_html=True)

                for a in r.get("assigns", []):
                    st.markdown(f"<div style='display:flex; justify-content:space-between; padding:6px 8px; margin-top:4px; background:#f5f5f0; border-radius:6px; font-size:0.8rem;'><span>{a['name']}</span><strong>{a['buf']:.1f}</strong></div>", unsafe_allow_html=True)

    # Team management section - toggle with button
    st.markdown("---")
    if "show_team_mgmt" not in st.session_state:
        st.session_state.show_team_mgmt = False

    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        label = "Hide Team Assignments" if st.session_state.show_team_mgmt else "Manage Team Assignments"
        if st.button(label, use_container_width=True):
            st.session_state.show_team_mgmt = not st.session_state.show_team_mgmt
            st.rerun()

    if st.session_state.show_team_mgmt:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        for dev in DEVELOPERS:
            c1, c2 = st.columns([2, 2])
            with c1:
                st.write(dev["name"])
            with c2:
                current = team_assignments.get(dev["id"], "team1")
                current_idx = next((i for i, t in enumerate(TEAMS) if t["id"] == current), 0)
                new_team = st.selectbox(
                    "",
                    [t["name"] for t in TEAMS],
                    index=current_idx,
                    key=f"team_assign_{dev['id']}",
                    label_visibility="collapsed"
                )
                new_id = next(t["id"] for t in TEAMS if t["name"] == new_team)
                if new_id != current:
                    save_team_assignment(dev["id"], new_id)
                    st.rerun()

def page_add_sprint():
    # Use cached data - no DB calls on +/- clicks
    team_assignments = get_team_assignments()

    # Initialize session state for sprint form
    if "sprint_pts" not in st.session_state:
        st.session_state.sprint_pts = {d["id"]: 0.0 for d in DEVELOPERS}
    if "sprint_pto" not in st.session_state:
        st.session_state.sprint_pto = {d["id"]: 0.0 for d in DEVELOPERS}

    # Sprint info
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("Sprint Name")
    with c2:
        start = st.date_input("Start")
    with c3:
        end = st.date_input("End", value=date.today() + timedelta(days=13))

    hols = get_holidays(start, end) if start and end else []
    if hols:
        st.info(f"Holidays: {', '.join(h['name'] for h in hols)}")

    st.markdown("---")
    st.markdown("<h4 style='text-align:center; color:#4a4a4a; font-weight:600; margin-bottom:16px;'>Developer Points</h4>", unsafe_allow_html=True)

    # Column headers
    header_cols = st.columns([1, 0.3, 1])
    for col_idx in [0, 2]:
        with header_cols[col_idx]:
            _, h1, h2, h3 = st.columns([2, 1, 1, 1])
            with h1: st.markdown("<div style='font-size:0.7rem; color:#aaa; text-transform:uppercase; letter-spacing:0.05em; text-align:center;'>Pts</div>", unsafe_allow_html=True)
            with h2: st.markdown("<div style='font-size:0.7rem; color:#aaa; text-transform:uppercase; letter-spacing:0.05em; text-align:center;'>PTO</div>", unsafe_allow_html=True)
            with h3: st.markdown("<div style='font-size:0.7rem; color:#aaa; text-transform:uppercase; letter-spacing:0.05em; text-align:center;'>Team</div>", unsafe_allow_html=True)

    # Developer rows - 2 columns with gap
    for i in range(0, len(DEVELOPERS), 2):
        row_cols = st.columns([1, 0.3, 1])
        col_indices = [0, 2]  # Skip spacer column
        for j, col_idx in enumerate(col_indices):
            if i + j < len(DEVELOPERS):
                dev = DEVELOPERS[i + j]
                dev_id = dev["id"]
                with row_cols[col_idx]:
                    pts = st.session_state.sprint_pts.get(dev_id, 0.0)
                    pto = st.session_state.sprint_pto.get(dev_id, 0.0)
                    name_col, left, mid, right = st.columns([2, 1, 1, 1])
                    with name_col:
                        st.markdown(f"**{dev['name'].split()[0]}**")
                    with left:
                        new_pts = st.number_input(
                            "Points", value=pts, min_value=0.0, step=0.5,
                            format="%.1f", key=f"sp_{dev_id}", label_visibility="collapsed"
                        )
                        if new_pts != pts:
                            st.session_state.sprint_pts[dev_id] = new_pts
                            st.rerun()
                    with mid:
                        new_pto = st.number_input(
                            "PTO", value=pto, min_value=0.0, max_value=10.0, step=0.5,
                            format="%.1f", key=f"pto_sprint_{dev_id}", label_visibility="collapsed"
                        )
                        if new_pto != pto:
                            st.session_state.sprint_pto[dev_id] = new_pto
                            st.rerun()
                    with right:
                        dt = team_assignments.get(dev_id, "team1")
                        di = next((idx for idx, t in enumerate(TEAMS) if t["id"] == dt), 0)
                        st.selectbox("Team", [t["name"] for t in TEAMS], di, key=f"tm_{dev_id}", label_visibility="collapsed")

        # Divider between developer rows
        st.markdown("<div style='border-top:1px solid #e8e8e3; margin:10px 0 8px;'></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Save button
    if st.button("Save Sprint", type="primary", use_container_width=True):
        assigns = []
        for dev in DEVELOPERS:
            pts = st.session_state.sprint_pts.get(dev["id"], 0)
            pto = st.session_state.sprint_pto.get(dev["id"], 0)
            tm_name = st.session_state.get(f"tm_{dev['id']}", TEAMS[0]["name"])
            tid = next((t["id"] for t in TEAMS if t["name"] == tm_name), "team1")
            if pts > 0:
                assigns.append({"engineerId": dev["id"], "teamId": tid, "storyPoints": pts, "totalPtoDays": pto})

        if not name:
            st.error("Enter sprint name")
        elif not assigns:
            st.error("Enter points for at least one dev")
        else:
            bd = sum(1 for d in range((end - start).days + 1) if (start + timedelta(days=d)).weekday() < 5)
            sprint = {"sprintId": f"{start.year}-S{start.month:02d}-{start.day:02d}", "sprintName": name,
                      "startDate": start.isoformat(), "endDate": end.isoformat(), "sprintDays": bd, "assignments": assigns}
            # Check if this sprint already exists (for user feedback)
            existing_check = supabase.table("sprints").select("sprint_id").eq("sprint_name", name).execute()
            is_update = bool(existing_check.data)
            if save_sprint(sprint):
                st.success(f"'{name}' {'updated' if is_update else 'saved'}!")
                # Invalidate cache and reset form
                st.session_state.sprints_cache = None
                st.session_state.sprint_pts = {d["id"]: 0.0 for d in DEVELOPERS}
                st.session_state.sprint_pto = {d["id"]: 0.0 for d in DEVELOPERS}
                st.balloons()

def page_analytics():
    sprints = get_sprints()
    if not sprints:
        st.info("No sprint data yet.")
        return

    # Use cached team assignments to remap legacy Storyblok data
    team_assignments = get_team_assignments()

    def get_effective_team(assignment):
        """Map old storyblok assignments to current team based on developer's current assignment"""
        if assignment["teamId"] == "storyblok":
            return team_assignments.get(assignment["engineerId"], "team1")
        return assignment["teamId"]

    def team_pts(sprint, tid):
        """Sum points for a team, including remapped Storyblok assignments"""
        return sum(a["storyPoints"] for a in sprint.get("assignments", []) if get_effective_team(a) == tid)

    recent = sprints[:6]
    def avg(tid): return sum(team_pts(s, tid) for s in recent) / len(recent) if recent else 0

    cols = st.columns(3)
    overall = sum(sum(a["storyPoints"] for a in s.get("assignments", [])) for s in recent) / len(recent) if recent else 0

    for i, (lbl, val) in enumerate([("Overall", overall), ("Team 1", avg("team1")), ("Team 2", avg("team2"))]):
        with cols[i]:
            st.markdown(f'<div class="metric"><div class="label">{lbl}</div><div class="value">{val:.1f}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Chart - Storyblok data collapsed into current team assignments
    data = [{"Sprint": s["sprintName"],
             "Team 1": team_pts(s, "team1"),
             "Team 2": team_pts(s, "team2")}
            for s in reversed(sprints[:12])]
    df = pd.DataFrame(data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 1"], mode="lines+markers", name="Team 1", line=dict(color="#6b7c6b", width=2)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 2"], mode="lines+markers", name="Team 2", line=dict(color="#c17a5a", width=2)))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6", font=dict(color="#4a4a4a", size=11), height=280,
                      margin=dict(t=30, b=50, l=40, r=20), xaxis=dict(gridcolor="#e5e5e0", tickangle=-45), yaxis=dict(gridcolor="#e5e5e0", title="Pts"),
                      legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    tbl = [{"Sprint": s["sprintName"], "Period": f"{s['startDate']} → {s['endDate']}",
            "Team 1": team_pts(s, "team1"),
            "Team 2": team_pts(s, "team2")} for s in sprints[:10]]
    st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

def page_individual():
    sprints = get_sprints()
    if not sprints:
        st.info("No sprint data yet.")
        return

    sel = st.selectbox("Developer", ["Select..."] + [d["name"] for d in DEVELOPERS])
    if sel == "Select...":
        st.caption("Select a developer to view metrics.")
        return

    dev = next((d for d in DEVELOPERS if d["name"] == sel), None)
    if not dev: return

    st.markdown("---")

    agg = {}
    for s in sprints:
        for a in s.get("assignments", []):
            if a["engineerId"] == dev["id"]:
                if s["sprintId"] not in agg:
                    agg[s["sprintId"]] = {"sprintId": s["sprintId"], "sprintName": s["sprintName"], "startDate": s["startDate"],
                                          "endDate": s["endDate"], "sprintDays": s["sprintDays"], "storyPoints": 0, "totalPtoDays": 0}
                agg[s["sprintId"]]["storyPoints"] += a["storyPoints"]
                agg[s["sprintId"]]["totalPtoDays"] = max(agg[s["sprintId"]]["totalPtoDays"], a.get("totalPtoDays", 0))

    data = sorted(agg.values(), key=lambda x: x["startDate"], reverse=True)
    vel = calc_velocity(data)

    cols = st.columns(3)
    with cols[0]: st.markdown(f'<div class="metric"><div class="label">Velocity</div><div class="value">{vel:.2f}</div></div>', unsafe_allow_html=True)
    with cols[1]: st.markdown(f'<div class="metric"><div class="label">Last 10</div><div class="value">{sum(d["storyPoints"] for d in data[:10]):.1f}</div></div>', unsafe_allow_html=True)
    with cols[2]: st.markdown(f'<div class="metric"><div class="label">Sprints</div><div class="value">{len(data)}</div></div>', unsafe_allow_html=True)

    if data:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        chart = [{"Sprint": d["sprintName"], "Vel": d["storyPoints"] / (d["sprintDays"] - d["totalPtoDays"]) if d["sprintDays"] - d["totalPtoDays"] > 0 else 0} for d in reversed(data[:10])]
        df = pd.DataFrame(chart)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Vel"], mode="lines+markers", line=dict(color="#6b7c6b", width=2), fill="tozeroy", fillcolor="rgba(107,124,107,0.1)"))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6", font=dict(color="#4a4a4a"), height=200,
                          margin=dict(t=10, b=50, l=40, r=20), showlegend=False, xaxis=dict(gridcolor="#e5e5e0", tickangle=-45), yaxis=dict(gridcolor="#e5e5e0", title="pts/day"))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        tbl = [{"Sprint": d["sprintName"], "Date": d["startDate"][:10], "Pts": d["storyPoints"], "PTO": d["totalPtoDays"]} for d in data[:15]]
        st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

# ============== MAIN ==============
def main():
    st.markdown('<div class="header"><h1>✦ Sprint Velocity ✦</h1><p>CHG Web Product Team</p></div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["Forecast", "Add Sprint", "Analytics", "Individual"])
    with t1: page_forecast()
    with t2: page_add_sprint()
    with t3: page_analytics()
    with t4: page_individual()

if __name__ == "__main__":
    main()

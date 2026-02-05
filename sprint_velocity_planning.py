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
    page_icon="⚡",
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

# ============== CUSTOM CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .main, .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0a0f1a 0%, #0f172a 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    h1, h2, h3, h4, h5, h6 { font-family: 'Inter', sans-serif !important; font-weight: 600 !important; }
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(71, 85, 105, 0.4);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(71, 85, 105, 0.4);
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
    }
    .metric-value { font-size: 2.5rem; font-weight: 700; line-height: 1.2; margin: 8px 0; }
    .metric-label { font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8; }
    .metric-sublabel { font-size: 0.8rem; color: #64748b; }
    .accent-orange { color: #fb923c; }
    .accent-green { color: #22c55e; }
    .accent-cyan { color: #06b6d4; }
    .bg-orange { background: linear-gradient(135deg, rgba(251, 146, 60, 0.15) 0%, rgba(251, 146, 60, 0.05) 100%); border: 1px solid rgba(251, 146, 60, 0.3); }
    .bg-green { background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%); border: 1px solid rgba(34, 197, 94, 0.3); }
    .bg-cyan { background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(6, 182, 212, 0.05) 100%); border: 1px solid rgba(6, 182, 212, 0.3); }
    .app-header { text-align: center; padding: 32px 0 24px 0; }
    .app-title {
        font-size: 2.25rem; font-weight: 700;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .app-subtitle { color: #64748b; font-size: 0.95rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: rgba(15, 23, 42, 0.6); padding: 6px; border-radius: 12px; justify-content: center; border: 1px solid rgba(71, 85, 105, 0.3); }
    .stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; padding: 12px 24px; font-weight: 500; color: #94a3b8; border: none; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important; color: white !important; }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
    .stButton > button { background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%); color: white; border: none; border-radius: 10px; padding: 12px 24px; font-weight: 600; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4); }
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(71, 85, 105, 0.5) !important; border-radius: 10px !important; color: #f1f5f9 !important;
    }
    .section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
    .section-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
    .section-title { font-size: 1.5rem; font-weight: 600; color: #f1f5f9; margin: 0; }
    .forecast-card { border-radius: 16px; padding: 28px; text-align: center; position: relative; overflow: hidden; }
    .forecast-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; }
    .forecast-card.orange::before { background: linear-gradient(90deg, #fb923c, #f97316); }
    .forecast-card.green::before { background: linear-gradient(90deg, #22c55e, #16a34a); }
    .forecast-card.cyan::before { background: linear-gradient(90deg, #06b6d4, #0891b2); }
    .forecast-team-name { font-size: 1.1rem; font-weight: 600; margin-bottom: 4px; }
    .forecast-raw { color: #64748b; font-size: 0.85rem; margin-bottom: 16px; }
    .forecast-value { font-size: 3.5rem; font-weight: 700; line-height: 1; margin-bottom: 8px; }
    .forecast-buffer { color: #64748b; font-size: 0.8rem; }
    .breakdown-item { background: rgba(51, 65, 85, 0.4); border-radius: 10px; padding: 14px 16px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; }
    .breakdown-name { font-weight: 500; color: #e2e8f0; font-size: 0.9rem; }
    .breakdown-meta { color: #64748b; font-size: 0.75rem; margin-top: 2px; }
    .breakdown-value { font-weight: 700; font-size: 1.1rem; color: #f1f5f9; }
    hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(71, 85, 105, 0.5), transparent); margin: 24px 0; }
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

TEAM_COLORS = {"orange": "#fb923c", "green": "#22c55e", "cyan": "#06b6d4"}

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
        # Insert sprint
        supabase.table("sprints").insert({
            "sprint_id": sprint_data["sprintId"],
            "sprint_name": sprint_data["sprintName"],
            "start_date": sprint_data["startDate"],
            "end_date": sprint_data["endDate"],
            "sprint_days": sprint_data["sprintDays"]
        }).execute()

        # Insert assignments
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
        # Default assignments if table doesn't exist yet
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
    st.markdown('<div class="section-header"><div class="section-icon">📊</div><h2 class="section-title">Sprint Forecast</h2></div>', unsafe_allow_html=True)

    team_assignments = load_team_assignments()
    sprints = load_sprints()

    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        buffer_opts = {"70% (Conservative)": 0.70, "85% (Standard)": 0.85, "100% (Aggressive)": 1.00}
        sel = st.selectbox("Planning Buffer", list(buffer_opts.keys()), index=1)
        st.session_state.planning_buffer = buffer_opts[sel]
    with col3:
        calc = st.button("⚡ Calculate", type="primary", use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 👥 Team Assignments & PTO")

    cols = st.columns(len(TEAMS))
    for idx, team in enumerate(TEAMS):
        with cols[idx]:
            color = TEAM_COLORS.get(team["color"], "#fb923c")
            devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team["id"]]

            st.markdown(f'''
            <div class="glass-card bg-{team['color']}" style="border-radius:16px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><h4 style="color:{color};margin:0;">{team['name']}</h4><p style="color:#64748b;margin:4px 0 0 0;font-size:0.85rem;">{team['pmName']}</p></div>
                    <span style="background:rgba(0,0,0,0.2);padding:4px 10px;border-radius:12px;color:#94a3b8;font-size:0.75rem;">{len(devs)} devs</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            for dev in devs:
                st.markdown(f"**{dev['name']}**")
                c1, c2 = st.columns([3, 1])
                with c1:
                    pto = st.number_input("PTO", 0.0, 10.0, st.session_state.pto_data.get(dev["id"], 0.0), 0.5, key=f"pto_{dev['id']}", label_visibility="collapsed")
                    st.session_state.pto_data[dev["id"]] = pto
                with c2:
                    others = [t for t in TEAMS if t["id"] != team["id"]]
                    mv = st.selectbox("→", [""] + [t["name"] for t in others], key=f"mv_{dev['id']}", label_visibility="collapsed")
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
        st.markdown("### 📈 Forecast Results")
        f = st.session_state.forecast
        cols = st.columns(len(TEAMS))
        for idx, team in enumerate(TEAMS):
            r = f["teams"].get(team["id"], {})
            color = TEAM_COLORS.get(r.get("color", "orange"), "#fb923c")
            with cols[idx]:
                st.markdown(f'''
                <div class="forecast-card bg-{team['color']} {team['color']}" style="border-radius:16px;">
                    <div class="forecast-team-name" style="color:{color};">{r.get('name', team['name'])}</div>
                    <div class="forecast-raw">Raw: {r.get('raw', 0):.1f} pts</div>
                    <div class="forecast-value" style="color:{color};">{r.get('buf', 0):.1f}</div>
                    <div class="forecast-buffer">points @ {int(f['buffer']*100)}% buffer</div>
                </div>
                ''', unsafe_allow_html=True)
                for a in r.get("assigns", []):
                    st.markdown(f'''
                    <div class="breakdown-item">
                        <div><div class="breakdown-name">{a['name']}</div><div class="breakdown-meta">{a['vel']:.2f} pts/day · {a['wd']:.0f} days</div></div>
                        <div class="breakdown-value">{a['buf']:.1f}</div>
                    </div>
                    ''', unsafe_allow_html=True)

def render_add_sprint():
    st.markdown('<div class="section-header"><div class="section-icon">➕</div><h2 class="section-title">Add Sprint Data</h2></div>', unsafe_allow_html=True)

    team_assignments = load_team_assignments()

    with st.form("add_sprint"):
        c1, c2, c3 = st.columns(3)
        with c1: name = st.text_input("Sprint Name", placeholder="e.g., Suttungr")
        with c2: start = st.date_input("Start Date")
        with c3: end = st.date_input("End Date", value=date.today() + timedelta(days=13))

        if start and end:
            hols = get_holidays_in_range(start, end)
            if hols: st.info(f"🗓️ Holidays: {', '.join(h['name'] for h in hols)}")

        st.markdown("### Developer Contributions")
        assigns = []
        for i in range(0, len(DEVELOPERS), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(DEVELOPERS):
                    dev = DEVELOPERS[i + j]
                    with col:
                        st.markdown(f"**👤 {dev['name']}**")
                        c1, c2, c3 = st.columns(3)
                        with c1: pts = st.number_input("Points", 0.0, step=0.5, key=f"sp_{dev['id']}")
                        with c2: pto = st.number_input("PTO", 0.0, 10.0, step=0.5, key=f"pto_a_{dev['id']}")
                        with c3:
                            teams = [t["name"] for t in TEAMS]
                            dt = team_assignments.get(dev["id"], "team1")
                            di = next((idx for idx, t in enumerate(TEAMS) if t["id"] == dt), 0)
                            tm = st.selectbox("Team", teams, di, key=f"tm_{dev['id']}")
                        if pts > 0:
                            tid = next(t["id"] for t in TEAMS if t["name"] == tm)
                            assigns.append({"engineerId": dev["id"], "teamId": tid, "storyPoints": pts, "totalPtoDays": pto})
                        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        if st.form_submit_button("💾 Save Sprint", type="primary", use_container_width=True):
            if not name: st.error("Enter sprint name")
            elif not assigns: st.error("Enter points for at least one dev")
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
                    st.success(f"✅ '{name}' saved!")
                    st.balloons()

def render_team_analytics():
    st.markdown('<div class="section-header"><div class="section-icon">📈</div><h2 class="section-title">Team Analytics</h2></div>', unsafe_allow_html=True)

    sprints = load_sprints()
    if not sprints:
        st.info("No sprint data yet. Add your first sprint!")
        return

    recent = sprints[:6]
    def avg(tid): return sum(sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == tid) for s in recent) / len(recent) if recent else 0

    c1, c2, c3, c4 = st.columns(4)
    overall = sum(sum(a["storyPoints"] for a in s.get("assignments", [])) for s in recent) / len(recent) if recent else 0
    with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Overall</div><div class="metric-value" style="color:#f1f5f9;">{overall:.1f}</div><div class="metric-sublabel">pts/sprint</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card bg-orange"><div class="metric-label">Team 1</div><div class="metric-value accent-orange">{avg("team1"):.1f}</div><div class="metric-sublabel">pts/sprint</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card bg-green"><div class="metric-label">Team 2</div><div class="metric-value accent-green">{avg("team2"):.1f}</div><div class="metric-sublabel">pts/sprint</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card bg-cyan"><div class="metric-label">Storyblok</div><div class="metric-value accent-cyan">{avg("storyblok"):.1f}</div><div class="metric-sublabel">pts/sprint</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    data = [{"Sprint": s["sprintName"], "Team 1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
             "Team 2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
             "Storyblok": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")} for s in reversed(sprints[:12])]
    df = pd.DataFrame(data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 1"], mode="lines+markers", name="Team 1", line=dict(color="#fb923c", width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 2"], mode="lines+markers", name="Team 2", line=dict(color="#22c55e", width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Storyblok"], mode="lines+markers", name="Storyblok", line=dict(color="#06b6d4", width=3), marker=dict(size=8)))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.3)", font_color="#e2e8f0", height=350,
                      xaxis=dict(gridcolor="rgba(71,85,105,0.3)"), yaxis=dict(gridcolor="rgba(71,85,105,0.3)", title="Story Points"),
                      legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Recent Sprints")
    tbl = [{"Sprint": s["sprintName"], "Period": f"{s['startDate']} → {s['endDate']}",
            "🟠 T1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
            "🟢 T2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
            "🔵 SB": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")} for s in sprints[:10]]
    st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

def render_individual():
    st.markdown('<div class="section-header"><div class="section-icon">👤</div><h2 class="section-title">Individual Analytics</h2></div>', unsafe_allow_html=True)

    sprints = load_sprints()
    if not sprints:
        st.info("No sprint data yet.")
        return

    sel = st.selectbox("Select Developer", ["Choose..."] + [d["name"] for d in DEVELOPERS])
    if sel == "Choose...":
        st.markdown("#### Select a developer above")
        return

    dev = next((d for d in DEVELOPERS if d["name"] == sel), None)
    if not dev: return

    st.markdown(f"### {dev['name']}")
    st.caption(dev["role"])

    agg = {}
    for s in sprints:
        for a in s.get("assignments", []):
            if a["engineerId"] == dev["id"]:
                if s["sprintId"] not in agg:
                    agg[s["sprintId"]] = {"sprintId": s["sprintId"], "sprintName": s["sprintName"], "startDate": s["startDate"], "endDate": s["endDate"], "sprintDays": s["sprintDays"], "storyPoints": 0, "totalPtoDays": 0, "teams": []}
                agg[s["sprintId"]]["storyPoints"] += a["storyPoints"]
                agg[s["sprintId"]]["totalPtoDays"] = max(agg[s["sprintId"]]["totalPtoDays"], a.get("totalPtoDays", 0))
                agg[s["sprintId"]]["teams"].append(a["teamId"])

    data = sorted(agg.values(), key=lambda x: x["startDate"], reverse=True)
    vel = calculate_velocity(data)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Velocity</div><div class="metric-value" style="color:#3b82f6;">{vel:.2f}</div><div class="metric-sublabel">pts/day</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Points</div><div class="metric-value" style="color:#f1f5f9;">{sum(d["storyPoints"] for d in data):.1f}</div><div class="metric-sublabel">all time</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">Sprints</div><div class="metric-value" style="color:#f1f5f9;">{len(data)}</div><div class="metric-sublabel">tracked</div></div>', unsafe_allow_html=True)

    if data:
        chart = [{"Sprint": d["sprintName"], "Velocity": d["storyPoints"] / (d["sprintDays"] - d["totalPtoDays"]) if d["sprintDays"] - d["totalPtoDays"] > 0 else 0} for d in reversed(data[:10])]
        df = pd.DataFrame(chart)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Velocity"], mode="lines+markers", line=dict(color="#3b82f6", width=3), marker=dict(size=10), fill="tozeroy", fillcolor="rgba(59,130,246,0.1)"))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30,41,59,0.3)", font_color="#e2e8f0", height=280,
                          xaxis=dict(gridcolor="rgba(71,85,105,0.3)"), yaxis=dict(gridcolor="rgba(71,85,105,0.3)", title="pts/day"), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Sprint History")
        tbl = [{"Sprint": d["sprintName"], "Date": d["startDate"][:10], "Teams": ",".join(set("T1" if t=="team1" else "T2" if t=="team2" else "SB" for t in d["teams"])),
                "Points": d["storyPoints"], "PTO": d["totalPtoDays"], "Velocity": f"{d['storyPoints']/(d['sprintDays']-d['totalPtoDays']):.2f}" if d["sprintDays"]-d["totalPtoDays"]>0 else "0"} for d in data[:15]]
        st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

# ============== MAIN ==============
def main():
    st.markdown('<div class="app-header"><h1 class="app-title">⚡ Sprint Velocity Planning</h1><p class="app-subtitle">CHG Web Product Team</p></div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["📊 Forecast", "➕ Add Sprint", "📈 Team Analytics", "👤 Individual"])
    with t1: render_forecast()
    with t2: render_add_sprint()
    with t3: render_team_analytics()
    with t4: render_individual()

if __name__ == "__main__":
    main()

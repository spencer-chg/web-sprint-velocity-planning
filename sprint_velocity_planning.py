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

# ============== MINIMAL CLEAN CSS ==============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Base */
:root { --sage: #6b7c6b; --cream: #f5f5f0; }
html, body, .stApp, [data-testid="stAppViewContainer"] { background: #f5f5f0 !important; }
.stApp > header { background: transparent !important; }
#MainMenu, footer, .stDeployButton { display: none !important; }
* { font-family: 'Inter', -apple-system, sans-serif !important; }
.block-container { max-width: 920px !important; padding: 1rem 1rem 3rem !important; }

/* Header */
.header { text-align: center; padding: 20px 0 16px; }
.header h1 { font-size: 1.4rem; font-weight: 600; color: #3a3a3a; margin: 0; }
.header p { font-size: 0.7rem; color: #888; margin: 4px 0 0; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { justify-content: center; border-bottom: 1px solid #e5e5e0; gap: 0; }
.stTabs [data-baseweb="tab"] { color: #888 !important; font-size: 0.85rem !important; padding: 10px 20px !important; }
.stTabs [aria-selected="true"] { color: #6b7c6b !important; border-bottom: 2px solid #6b7c6b !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* Team Card */
.team-card { background: white; border-radius: 14px; padding: 16px 18px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.team-card h3 { font-size: 0.9rem; font-weight: 600; color: #6b7c6b; margin: 0 0 2px; }
.team-card p { font-size: 0.7rem; color: #999; margin: 0; }

/* Dev Row */
.dev-row { display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #f0f0eb; }
.dev-row:last-child { border-bottom: none; }
.dev-name { flex: 1; font-size: 0.85rem; font-weight: 500; color: #4a4a4a; }
.pto-control { display: flex; align-items: center; gap: 2px; }
.pto-btn { width: 32px; height: 32px; border-radius: 8px; border: none; background: #6b7c6b; color: white; font-size: 1.1rem; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.pto-btn:hover { background: #5a6a5a; }
.pto-val { width: 44px; text-align: center; font-weight: 600; font-size: 0.85rem; color: #4a4a4a; padding: 6px 0; background: #f5f5f0; border-radius: 6px; margin: 0 2px; }
.move-link { font-size: 0.75rem; color: #999; margin-left: 12px; cursor: pointer; }
.move-link:hover { color: #6b7c6b; }

/* ALL buttons sage green */
.stButton button,
.stButton > button,
.stButton button[kind],
.stButton button[data-testid],
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"],
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    background: #6b7c6b !important;
    background-color: #6b7c6b !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0 !important;
    height: 36px !important;
    min-height: 36px !important;
    line-height: 36px !important;
}
.stButton button:hover,
.stButton > button:hover,
[data-testid="baseButton-secondary"]:hover,
[data-testid="baseButton-primary"]:hover {
    background: #5a6a5a !important;
    background-color: #5a6a5a !important;
}

/* Align all column content - pixel perfect spacing */
[data-testid="column"] { display: flex; align-items: center; justify-content: center; }
[data-testid="column"] > div { width: 100%; display: flex; justify-content: center; }
[data-testid="column"] .stButton { display: flex; justify-content: center; width: 100%; }
[data-testid="column"] .stButton > button { margin: 0 auto; }
[data-testid="column"] .stNumberInput { width: 100%; }
[data-testid="column"] .stNumberInput > div { margin: 0 auto; }

/* Equal gaps around value box */
.stNumberInput [data-baseweb="input"] { margin: 0 4px; }

/* Selectbox */
.stSelectbox > div > div {
    background: white !important;
    border: 1px solid #e5e5e0 !important;
    border-radius: 8px !important;
}

/* Forecast card */
.forecast-card { background: white; border-radius: 14px; padding: 20px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.forecast-card .label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.05em; color: #999; }
.forecast-card .value { font-size: 2rem; font-weight: 700; color: #6b7c6b; }
.forecast-card .sub { font-size: 0.7rem; color: #aaa; }

/* Metric */
.metric { background: white; border-radius: 10px; padding: 16px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.metric .label { font-size: 0.65rem; text-transform: uppercase; color: #999; }
.metric .value { font-size: 1.5rem; font-weight: 700; color: #6b7c6b; }

/* Form inputs */
.stTextInput input, .stDateInput input { background: white !important; border: 1px solid #e5e5e0 !important; border-radius: 8px !important; }

/* Form container styling */
[data-testid="stForm"] {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    border: none !important;
}

/* Number input - sage green buttons everywhere */
.stNumberInput input,
[data-testid="stNumberInput"] input {
    background: white !important;
    border: none !important;
    text-align: center !important;
    font-weight: 600 !important;
    color: #4a4a4a !important;
}
.stNumberInput [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"] {
    background: white !important;
    border: 1px solid #e5e5e0 !important;
    border-radius: 8px !important;
}
.stNumberInput button,
.stNumberInput [data-testid="stNumberInputStepUp"],
.stNumberInput [data-testid="stNumberInputStepDown"],
[data-testid="stNumberInput"] button,
[data-baseweb="input"] button {
    background: #6b7c6b !important;
    background-color: #6b7c6b !important;
    color: white !important;
    border: none !important;
}
.stNumberInput button:hover,
[data-testid="stNumberInput"] button:hover,
[data-baseweb="input"] button:hover {
    background: #5a6a5a !important;
    background-color: #5a6a5a !important;
}
.stNumberInput button:first-of-type,
[data-testid="stNumberInput"] button:first-of-type {
    border-radius: 8px 0 0 8px !important;
}
.stNumberInput button:last-of-type,
[data-testid="stNumberInput"] button:last-of-type {
    border-radius: 0 8px 8px 0 !important;
}

/* Hide default hr styling issues */
hr { border: none; height: 1px; background: #e5e5e0; margin: 20px 0; }

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

TEAMS = [
    {"id": "team1", "name": "Team 1", "pm": "Jason & Spencer"},
    {"id": "team2", "name": "Team 2", "pm": "Matt & Matt"},
    {"id": "storyblok", "name": "Storyblok", "pm": "Storyblok"},
]

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
        supabase.table("sprints").insert({"sprint_id": data["sprintId"], "sprint_name": data["sprintName"],
            "start_date": data["startDate"], "end_date": data["endDate"], "sprint_days": data["sprintDays"]}).execute()
        for a in data["assignments"]:
            supabase.table("sprint_assignments").insert({"sprint_id": data["sprintId"], "engineer_id": a["engineerId"],
                "team_id": a["teamId"], "story_points": a["storyPoints"], "pto_days": a["totalPtoDays"]}).execute()
        return True
    except: return False

def load_team_assignments():
    try:
        result = supabase.table("team_assignments").select("*").execute()
        if result.data: return {r["engineer_id"]: r["team_id"] for r in result.data}
    except: pass
    return {"fredrik-svensson": "team1", "fernando-fernandez": "team1", "matthew-callison": "team1", "cody-worthen": "team1",
            "stephen-corry": "team2", "tom-sharrock": "team2", "brady-hession": "team2", "jaime-virrueta": "team2"}

def save_team_assignment(eng_id, team_id):
    try:
        supabase.table("team_assignments").delete().eq("engineer_id", eng_id).execute()
        supabase.table("team_assignments").insert({"engineer_id": eng_id, "team_id": team_id}).execute()
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

# ============== COMPONENTS ==============
def render_dev_row(dev):
    """Clean developer row: [Name] [−] [value] [+]"""
    dev_id = dev["id"]
    first = dev["name"].split()[0]
    pto = st.session_state.pto.get(dev_id, 0.0)

    cols = st.columns([2.5, 0.8, 1.4, 0.8])

    with cols[0]:
        st.markdown(f"**{first}**")

    with cols[1]:
        if st.button("－", key=f"m_{dev_id}"):
            st.session_state.pto[dev_id] = max(0, pto - 0.5)

    with cols[2]:
        val = st.number_input("", min_value=0.0, max_value=10.0, value=pto, step=0.5,
                              key=f"input_{dev_id}", label_visibility="collapsed", format="%.1f")
        st.session_state.pto[dev_id] = val

    with cols[3]:
        if st.button("＋", key=f"p_{dev_id}"):
            st.session_state.pto[dev_id] = min(10, pto + 0.5)

# ============== PAGES ==============
def page_forecast():
    team_assignments = load_team_assignments()
    sprints = load_sprints()

    # Buffer selector + Calculate button
    c1, c2 = st.columns([3, 1])
    with c1:
        buf_opts = {"85% (Standard)": 0.85, "70% (Conservative)": 0.70, "100% (Aggressive)": 1.0}
        sel = st.selectbox("Planning Buffer", list(buf_opts.keys()))
        st.session_state.buffer = buf_opts[sel]
    with c2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        calc_btn = st.button("Calculate", type="primary", use_container_width=True)

    st.markdown("---")

    # Team columns
    cols = st.columns(3)
    for i, team in enumerate(TEAMS):
        with cols[i]:
            devs = [d for d in DEVELOPERS if team_assignments.get(d["id"]) == team["id"]]

            # Team card header
            st.markdown(f"""
            <div class="team-card">
                <h3>{team['name']}</h3>
                <p>{team['pm']} · {len(devs)} devs</p>
            </div>
            """, unsafe_allow_html=True)

            # Developer rows
            if devs:
                for dev in devs:
                    render_dev_row(dev)
            else:
                st.caption("No developers")

    # Team management section
    st.markdown("---")
    st.markdown("<h4 style='text-align:center; color:#4a4a4a; font-weight:600; margin-bottom:16px;'>Manage Team Assignments</h4>", unsafe_allow_html=True)

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

    # Calculate
    if calc_btn:
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
        cols = st.columns(3)
        for i, team in enumerate(TEAMS):
            r = f["teams"].get(team["id"], {})
            with cols[i]:
                st.markdown(f"""
                <div class="forecast-card">
                    <div class="label">{team['name']}</div>
                    <div class="value">{r.get('buf', 0):.1f}</div>
                    <div class="sub">Raw: {r.get('raw', 0):.1f}</div>
                </div>
                """, unsafe_allow_html=True)

                for a in r.get("assigns", []):
                    st.markdown(f"<div style='display:flex; justify-content:space-between; padding:6px 8px; margin-top:4px; background:#f5f5f0; border-radius:6px; font-size:0.8rem;'><span>{a['name']}</span><strong>{a['buf']:.1f}</strong></div>", unsafe_allow_html=True)

def page_add_sprint():
    team_assignments = load_team_assignments()

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

    # Developer rows - 2 columns
    for i in range(0, len(DEVELOPERS), 2):
        row_cols = st.columns(2)
        for j, col in enumerate(row_cols):
            if i + j < len(DEVELOPERS):
                dev = DEVELOPERS[i + j]
                dev_id = dev["id"]
                with col:
                    st.markdown(f"**{dev['name']}**")

                    # Pts row: [−] [value] [+] | Team dropdown
                    c1, c2, c3, c4, c5 = st.columns([0.8, 1.4, 0.8, 0.2, 2.5])
                    pts = st.session_state.sprint_pts.get(dev_id, 0.0)

                    with c1:
                        if st.button("－", key=f"spm_{dev_id}"):
                            st.session_state.sprint_pts[dev_id] = max(0, pts - 0.5)
                            st.rerun()
                    with c2:
                        new_pts = st.number_input("Pts", min_value=0.0, value=pts, step=0.5,
                                                   key=f"spv_{dev_id}", label_visibility="collapsed", format="%.1f")
                        st.session_state.sprint_pts[dev_id] = new_pts
                    with c3:
                        if st.button("＋", key=f"spp_{dev_id}"):
                            st.session_state.sprint_pts[dev_id] = pts + 0.5
                            st.rerun()
                    with c5:
                        dt = team_assignments.get(dev_id, "team1")
                        di = next((idx for idx, t in enumerate(TEAMS) if t["id"] == dt), 0)
                        st.selectbox("Team", [t["name"] for t in TEAMS], di, key=f"tm_{dev_id}", label_visibility="collapsed")

        # Add spacing between developer rows
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

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
            if save_sprint(sprint):
                st.success(f"'{name}' saved!")
                # Reset form
                st.session_state.sprint_pts = {d["id"]: 0.0 for d in DEVELOPERS}
                st.session_state.sprint_pto = {d["id"]: 0.0 for d in DEVELOPERS}
                st.balloons()

def page_analytics():
    sprints = load_sprints()
    if not sprints:
        st.info("No sprint data yet.")
        return

    recent = sprints[:6]
    def avg(tid): return sum(sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == tid) for s in recent) / len(recent) if recent else 0

    cols = st.columns(4)
    overall = sum(sum(a["storyPoints"] for a in s.get("assignments", [])) for s in recent) / len(recent) if recent else 0

    for i, (lbl, val) in enumerate([("Overall", overall), ("Team 1", avg("team1")), ("Team 2", avg("team2")), ("Storyblok", avg("storyblok"))]):
        with cols[i]:
            st.markdown(f'<div class="metric"><div class="label">{lbl}</div><div class="value">{val:.1f}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Chart
    data = [{"Sprint": s["sprintName"],
             "Team 1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
             "Team 2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
             "Storyblok": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")}
            for s in reversed(sprints[:12])]
    df = pd.DataFrame(data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 1"], mode="lines+markers", name="Team 1", line=dict(color="#6b7c6b", width=2)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Team 2"], mode="lines+markers", name="Team 2", line=dict(color="#5a6a5a", width=2)))
    fig.add_trace(go.Scatter(x=df["Sprint"], y=df["Storyblok"], mode="lines+markers", name="Storyblok", line=dict(color="#999", width=2, dash="dot")))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#faf9f6", font=dict(color="#4a4a4a", size=11), height=280,
                      margin=dict(t=30, b=50, l=40, r=20), xaxis=dict(gridcolor="#e5e5e0", tickangle=-45), yaxis=dict(gridcolor="#e5e5e0", title="Pts"),
                      legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    tbl = [{"Sprint": s["sprintName"], "Period": f"{s['startDate']} → {s['endDate']}",
            "T1": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team1"),
            "T2": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "team2"),
            "SB": sum(a["storyPoints"] for a in s.get("assignments", []) if a["teamId"] == "storyblok")} for s in sprints[:10]]
    st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

def page_individual():
    sprints = load_sprints()
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

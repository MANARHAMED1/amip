import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import traceback
from datetime import datetime
from dashboard.icons import icon, logo_full, logo_icon

st.set_page_config(
    page_title="AMIP - Advanced Manufacturing Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":material/factory:",
)

# ── Global CSS ─────────────────────────────────────────────────────
st.html("""
<style>
* { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; }
code, pre, .mono { font-family: 'SF Mono', 'Cascadia Code', 'Consolas', 'Courier New', monospace; }

:root {
    --navy: #0B2545;
    --steel: #5B7B9A;
    --steel-bg: rgba(91,123,154,0.08);
    --green: #2E7D32;
    --green-bg: rgba(46,125,50,0.08);
    --orange: #ED6C02;
    --orange-bg: rgba(237,108,2,0.08);
    --red: #C62828;
    --red-bg: rgba(198,40,40,0.08);
    --bg: #F4F6F8;
    --card: #FFFFFF;
    --border: #E2E5E9;
    --text: #1C1E21;
    --text-dim: #5A6872;
    --text-muted: #8A95A0;
    --shadow: 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px -4px rgba(0,0,0,0.08);
    --shadow-lg: 0 8px 24px -6px rgba(0,0,0,0.10);
    --radius: 8px;
    --radius-lg: 12px;
    --transition: all 0.2s cubic-bezier(0.4,0,0.2,1);
    --transition-slow: all 0.35s cubic-bezier(0.4,0,0.2,1);
}

/* ── Global ── */
.stApp { background: var(--bg) !important; }
.block-container { padding-top: 0.5rem !important; padding-bottom: 1.5rem !important; max-width: 1500px !important; }
header[data-testid="stHeader"] { background: transparent !important; }
div[data-testid="stToolbar"] { display: none !important; }

main > div:first-child > div:first-child { gap: 0 !important; }

/* ── Card hover lift (applied to custom html cards) ── */
.card-lift {
    transition: var(--transition-slow);
}
.card-lift:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0B2545 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] > div:first-child { padding-top: 1rem !important; }
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 { color: #E2E8F0 !important; }

section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    margin: 0 !important;
    transition: var(--transition) !important;
    color: #E2E8F0 !important;
    font-family: system-ui, -apple-system, sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.12) !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
    background: linear-gradient(135deg, #0B2545, #1A3A5C) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25) !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] > div:first-child {
    background: white !important;
    border-color: white !important;
}
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    display: none !important;
}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6 {
    color: var(--text) !important;
    font-family: system-ui, -apple-system, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}
h1 { font-size: 1.5rem !important; }
h2 { font-size: 1.2rem !important; }
h3 { font-size: 1rem !important; }
p, span, li, label, div, td, th { font-family: system-ui, -apple-system, sans-serif !important; }

/* ── Metric Cards (base) ── */
[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 16px 18px !important;
    box-shadow: var(--shadow) !important;
    transition: var(--transition) !important;
    border-top: 3px solid !important;
    border-image: linear-gradient(90deg, #0B2545, #5B7B9A) 1 !important;
    border-image-slice: 1 !important;
}
[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetric"] label {
    color: var(--text-dim) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-family: 'Consolas', 'Courier New', monospace !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}
[data-testid="stMetric"] [data-testid="stMetricDelta"] > div {
    font-family: 'Consolas', 'Courier New', monospace !important;
    font-weight: 600 !important;
}

/* ── Inputs ── */
.stSelectbox label, .stDateInput label, .stTextInput label, .stMultiSelect label, .stSlider label, .stNumberInput label {
    color: var(--text-dim) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}
div[data-baseweb="select"] > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: system-ui, -apple-system, sans-serif !important;
    transition: var(--transition) !important;
}
div[data-baseweb="select"]:hover > div { border-color: var(--steel) !important; }
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--steel) !important;
    box-shadow: 0 0 0 3px var(--steel-bg) !important;
}
div[data-baseweb="popover"] ul {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    box-shadow: var(--shadow-lg) !important;
}
div[data-baseweb="popover"] ul li { color: var(--text) !important; transition: var(--transition) !important; }
div[data-baseweb="popover"] ul li:hover {
    background: var(--steel-bg) !important;
    color: var(--steel) !important;
}
.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: system-ui, -apple-system, sans-serif !important;
    transition: var(--transition) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--steel) !important;
    box-shadow: 0 0 0 3px var(--steel-bg) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #5B7B9A, #4A6A8A) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-family: system-ui, -apple-system, sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: var(--transition) !important;
    box-shadow: 0 1px 4px rgba(91,123,154,0.2) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4A6A8A, #3A5A7A) !important;
    box-shadow: 0 4px 12px rgba(91,123,154,0.3) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}
.stButton > button::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255,255,255,0.2);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.5s, height 0.5s;
}
.stButton > button:active::after {
    width: 200px;
    height: 200px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    background: var(--card) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-dim) !important;
    border-radius: 6px !important;
    padding: 10px 20px !important;
    font-family: system-ui, -apple-system, sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: var(--transition) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--steel) !important;
    background: var(--steel-bg) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #5B7B9A, #4A6A8A) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(91,123,154,0.2) !important;
}
.stTabs [data-baseweb="tab-highlight"] { background-color: transparent !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    transition: var(--transition) !important;
}
[data-testid="stDataFrame"]:hover {
    box-shadow: var(--shadow-md) !important;
}

/* ── Plotly (base styling only — animation rules below in Keyframes) ── */
.modebar { display: none !important; }
.js-plotly-plot .plotly .cursor-pointer { cursor: default !important; }

/* ── Alerts ── */
.stAlert > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    transition: var(--transition) !important;
}
.stAlert > div:hover {
    box-shadow: var(--shadow-md) !important;
}
.stError > div { background: var(--red-bg) !important; border-color: rgba(198,40,40,0.25) !important; }
.stWarning > div { background: var(--orange-bg) !important; border-color: rgba(237,108,2,0.25) !important; }
.stInfo > div { background: var(--steel-bg) !important; border-color: rgba(91,123,154,0.25) !important; }
.stSuccess > div { background: var(--green-bg) !important; border-color: rgba(46,125,50,0.25) !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-weight: 600 !important;
    transition: var(--transition) !important;
}
.streamlit-expanderHeader:hover {
    box-shadow: var(--shadow-md) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; transition: var(--transition); }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ── Code ── */
code {
    background: var(--bg) !important;
    color: var(--steel) !important;
    padding: 2px 5px !important;
    border-radius: 4px !important;
    font-size: 12px !important;
    border: 1px solid var(--border) !important;
}
pre {
    background: var(--navy) !important;
    border-radius: 8px !important;
    padding: 14px !important;
    color: #E2E8F0 !important;
}
pre code { background: transparent !important; color: inherit !important; border: none !important; }

/* ── Login Page ── */
.amip-login-bg {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
.amip-login-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 48px 40px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
}
.amip-login-logo {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #0B2545, #5B7B9A);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 12px rgba(79,70,229,0.3);
}

/* ── Keyframes ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes statusPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes alertPulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(198,40,40,0.15); }
    50% { box-shadow: 0 0 0 6px rgba(198,40,40,0.05); }
}
@keyframes chartEntrance {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes barGrow {
    from { transform: scaleY(0.01); }
    to { transform: scaleY(1); }
}

/* ── Animation Utility Classes ── */
.fade-in { animation: fadeSlideUp 0.4s cubic-bezier(0.4,0,0.2,1) both; }
.fade-in-1 { animation: fadeSlideUp 0.4s cubic-bezier(0.4,0,0.2,1) 0.05s both; }
.fade-in-2 { animation: fadeSlideUp 0.4s cubic-bezier(0.4,0,0.2,1) 0.10s both; }
.fade-in-3 { animation: fadeSlideUp 0.4s cubic-bezier(0.4,0,0.2,1) 0.15s both; }
.fade-in-4 { animation: fadeSlideUp 0.4s cubic-bezier(0.4,0,0.2,1) 0.20s both; }
.fade-in-5 { animation: fadeSlideUp 0.4s cubic-bezier(0.4,0,0.2,1) 0.25s both; }

/* ── Animated Header Gradient ── */
.animated-header {
    background: linear-gradient(135deg, #0B2545, #1A3A5C, #0B2545) !important;
    background-size: 200% 200% !important;
    animation: gradientShift 8s ease infinite !important;
}

/* ── Chart Entrance Wrapper ── */
.stPlotlyChart {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 10px !important;
    transition: var(--transition-slow) !important;
    animation: chartEntrance 0.5s cubic-bezier(0.4,0,0.2,1) both !important;
}
.stPlotlyChart:hover {
    box-shadow: var(--shadow-md) !important;
}

/* ── KPI Card Staggered Entrance ── */
[data-testid="stMetric"] {
    animation: fadeSlideUp 0.5s cubic-bezier(0.4,0,0.2,1) both !important;
}
[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.02s !important; }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.06s !important; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.10s !important; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.14s !important; }
[data-testid="stMetric"]:nth-child(5) { animation-delay: 0.18s !important; }
[data-testid="stMetric"]:nth-child(6) { animation-delay: 0.22s !important; }
</style>
""")


# ── Login Page ─────────────────────────────────────────────────────
def render_login():
    st.html("""
    <style>
    .stApp { background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%) !important; }
    .block-container { padding-top: 2rem !important; }
    </style>
    """)

    st.html("<div style='min-height:80px'></div>")

    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.html(f"""
        <div style="background:#FFFFFF;border-radius:16px;padding:48px 40px;
                    box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);text-align:center">
            {logo_full("l")}
            <div style="width:40px;height:2px;background:linear-gradient(90deg,#0B2545,#5B7B9A);
                        margin:12px auto 28px;border-radius:2px"></div>
        </div>
        """)

        st.html("<div style='height:12px'></div>")

        username = st.text_input("Username", key="login_user", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
        remember = st.checkbox("Remember me")

        st.html("<div style='height:8px'></div>")

        if st.button("Sign In", key="login_btn", width="stretch"):
            if username and password:
                import requests as _req
                try:
                    resp = _req.post("http://localhost:8000/api/auth/login",
                                     json={"username": username, "password": password},
                                     timeout=10)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.authenticated = True
                        st.session_state.jwt_token = data["token"]
                        st.session_state.username = data["user"]["username"]
                        st.session_state.full_name = data["user"]["full_name"]
                        st.session_state.user_role = data["user"]["role"]
                        st.rerun()
                    else:
                        detail = resp.json().get("detail", "Invalid credentials") if resp.headers.get("content-type","").startswith("application/json") else "Invalid credentials"
                        st.error(detail)
                except _req.exceptions.ConnectionError:
                    st.error("API unreachable - verify backend is running on port 8000")
                except Exception as e:
                    st.error(f"Login error: {e}")
            else:
                st.error("Please enter username and password")

        st.html("""
        <div style="margin-top:24px;text-align:center;color:#94A3B8;font-size:11px">
            AMM Manufacturing Intelligence Platform<br>
            <span style="opacity:0.6">v2.0 | Industrial IoT</span>
        </div>
        """)

    # Return dummy page to avoid error
    return "Vue d'ensemble"


# ── Check authentication ───────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    render_login()
    st.stop()

# ── Render Sidebar (with icons) ───────────────────────────────────
from dashboard.components import render_sidebar, render_global_filters, render_critical_alerts

page = render_sidebar()

# ── Header Bar ─────────────────────────────────────────────────────
now = datetime.now()
date_str = now.strftime("%d %b %Y")
time_str = now.strftime("%H:%M")

st.html(f'''
<div class="animated-header" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;padding:14px 22px;
            border-radius:var(--radius-lg);color:white">
    <div style="display:flex;align-items:center;gap:12px">
        <div style="width:36px;height:36px;background:rgba(255,255,255,0.15);border-radius:10px;
                    display:flex;align-items:center;justify-content:center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8"
                 stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 21h18"/>
                <path d="M5 21V7l5 3V5l5 3V5l3 3v10"/>
                <path d="M9 21v-4h2v4"/>
                <path d="M15 21v-4h2v4"/>
            </svg>
        </div>
        <div>
            <div style="font-size:18px;font-weight:800;font-family:system-ui,sans-serif;letter-spacing:-0.01em">{page}</div>
            <div style="font-size:11px;opacity:0.8;margin-top:1px;font-family:system-ui,sans-serif;letter-spacing:0.02em">AMM Manufacturing Intelligence Platform</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:16px">
        <div style="text-align:right">
            <div style="font-size:12px;font-weight:600;font-family:system-ui,sans-serif">{date_str}</div>
            <div style="font-size:11px;opacity:0.7;font-family:system-ui,sans-serif">{time_str}</div>
        </div>
        <div style="width:34px;height:34px;background:rgba(255,255,255,0.12);border-radius:8px;
                    display:flex;align-items:center;justify-content:center">
            <span style="color:white;font-size:12px;font-weight:700;font-family:system-ui,sans-serif">
                {st.session_state.get('full_name', st.session_state.get('username', 'A'))[0].upper()}
            </span>
        </div>
    </div>
</div>
''')

# ── Critical Alerts Banner (overview page only) ─────────────────────
if page == "Vue d'ensemble":
    try:
        render_critical_alerts()
    except Exception:
        pass

# ── Global Filters ─────────────────────────────────────────────────
try:
    render_global_filters()
except Exception as e:
    st.error(f"Filtres error: {e}")

# ── Render Page Module ─────────────────────────────────────────────
PAGES = {
    "Vue d'ensemble": "executive",
    "Machines": "machine",
    "Production": "production",
    "Qualite": "quality",
    "Inventaire": "inventory",
    "Outillage": "tool",
    "Maintenance": "maintenance",
}

try:
    import importlib
    mod = importlib.import_module(f"dashboard.modules.{PAGES[page]}")
    mod.render()
except Exception as e:
    st.error(f"Page error: {e}")
    st.code(traceback.format_exc())

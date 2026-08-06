"""Professional SVG icon library for AMIP dashboard."""

# -- Icon size presets --
_S = "width='16' height='16' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'"
_M = "width='20' height='20' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'"
_L = "width='24' height='24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'"
_XL = "width='32' height='32' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'"

# ── Manufacturing ──────────────────────────────────────────────────
def factory(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M3 21h18'/>"
            "<path d='M5 21V7l5 3V5l5 3V5l3 3v10'/>"
            "<path d='M9 21v-4h2v4'/>"
            "<path d='M15 21v-4h2v4'/>"
            "</svg>")

def gear(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='3'/>"
            "<path d='M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72 1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42'/>"
            "</svg>")

def wrench(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z'/>"
            "</svg>")

def gauge(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z'/>"
            "<path d='M12 6v1'/>"
            "<path d='M6.93 7.93l.7.7'/>"
            "<path d='M6 12h1'/>"
            "<path d='M16.24 7.93l-.7.7'/>"
            "<path d='M18 12h-1'/>"
            "<path d='M12 12l3-6'/>"
            "</svg>")

def ruler(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z'/>"
            "<path d='m15 5 4 4'/>"
            "</svg>")

# ── Data & Analytics ───────────────────────────────────────────────
def chart_bar(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<rect x='3' y='12' width='4' height='9' rx='1'/>"
            "<rect x='10' y='7' width='4' height='14' rx='1'/>"
            "<rect x='17' y='3' width='4' height='18' rx='1'/>"
            "</svg>")

def chart_line(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M3 3v18h18'/>"
            "<path d='M7 16l4-5 4 3 5-7'/>"
            "</svg>")

def chart_pie(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 12'/>"
            "<path d='M21 3v5h-5'/>"
            "</svg>")

# ── Status & Alerts ────────────────────────────────────────────────
def alert_triangle(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'/>"
            "<line x1='12' y1='9' x2='12' y2='13'/>"
            "<line x1='12' y1='17' x2='12.01' y2='17'/>"
            "</svg>")

def alert_circle(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<line x1='12' y1='8' x2='12' y2='12'/>"
            "<line x1='12' y1='16' x2='12.01' y2='16'/>"
            "</svg>")

def check_circle(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<path d='M9 12l2 2 4-4'/>"
            "</svg>")

def x_circle(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<path d='M15 9l-6 6'/>"
            "<path d='M9 9l6 6'/>"
            "</svg>")

def circle_dot(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<circle cx='12' cy='12' r='3' fill='currentColor'/>"
            "</svg>")

# ── Production & Orders ────────────────────────────────────────────
def clipboard_list(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<rect x='8' y='2' width='8' height='4' rx='1' ry='1'/>"
            "<path d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/>"
            "<path d='M12 11h4'/>"
            "<path d='M12 16h4'/>"
            "<path d='M8 11h.01'/>"
            "<path d='M8 16h.01'/>"
            "</svg>")

def clipboard_check(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<rect x='8' y='2' width='8' height='4' rx='1' ry='1'/>"
            "<path d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/>"
            "<path d='M9 14l2 2 4-4'/>"
            "</svg>")

def timer(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<polyline points='12 6 12 12 16 14'/>"
            "</svg>")

def clock(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<polyline points='12 6 12 12 16 14'/>"
            "</svg>")

def history(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8'/>"
            "<path d='M3 3v5h5'/>"
            "<path d='M12 7v5l4 2'/>"
            "</svg>")

def package_icon(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M16.5 9.4 7.55 4.24'/>"
            "<path d='M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'/>"
            "<polyline points='3.27 6.96 12 12.01 20.73 6.96'/>"
            "<line x1='12' y1='22.08' x2='12' y2='12'/>"
            "</svg>")

def box(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'/>"
            "<path d='m3.27 6.96 8.73 5.05 8.73-5.05'/>"
            "<path d='M12 22.08V12'/>"
            "</svg>")

def coins(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='8' cy='8' r='6'/>"
            "<path d='M18.09 10.37A6 6 0 1 1 10.34 18'/>"
            "<path d='M7 6h2v4'/>"
            "<path d='M16 16h2v-2h1a1 1 0 1 0 0-2h-1'/>"
            "</svg>")

# ── Sensors & Equipment ────────────────────────────────────────────
def thermometer(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0z'/>"
            "</svg>")

def activity(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<polyline points='22 12 18 12 15 21 9 3 6 12 2 12'/>"
            "</svg>")

def zap(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<polygon points='13 2 3 14 12 14 11 22 21 10 12 10 13 2'/>"
            "</svg>")

def refresh(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<polyline points='23 4 23 10 17 10'/>"
            "<path d='M20.49 15a9 9 0 1 1-2.12-9.36L23 10'/>"
            "</svg>")

def target(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<circle cx='12' cy='12' r='6'/>"
            "<circle cx='12' cy='12' r='2' fill='currentColor'/>"
            "</svg>")

def shield(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/>"
            "<path d='M9 12l2 2 4-4'/>"
            "</svg>")

def shield_alert(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/>"
            "<line x1='12' y1='8' x2='12' y2='12'/>"
            "<line x1='12' y1='16' x2='12.01' y2='16'/>"
            "</svg>")

def settings(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='3'/>"
            "<path d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z'/>"
            "</svg>")

def bot(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<rect x='3' y='11' width='18' height='10' rx='2'/>"
            "<circle cx='12' cy='5' r='2'/>"
            "<path d='M12 7v4'/>"
            "<circle cx='8' cy='16' r='1' fill='currentColor'/>"
            "<circle cx='16' cy='16' r='1' fill='currentColor'/>"
            "</svg>")

def users(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/>"
            "<circle cx='9' cy='7' r='4'/>"
            "<path d='M22 21v-2a4 4 0 0 0-3-3.87'/>"
            "<path d='M16 3.13a4 4 0 0 1 0 7.75'/>"
            "</svg>")

# ── Interface ──────────────────────────────────────────────────────
def search(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='11' cy='11' r='8'/>"
            "<path d='M21 21l-4.35-4.35'/>"
            "</svg>")

def filter_icon(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<polygon points='22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3'/>"
            "</svg>")

def chevron_left(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<polyline points='15 18 9 12 15 6'/>"
            "</svg>")

def chevron_right(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<polyline points='9 18 15 12 9 6'/>"
            "</svg>")

def arrow_up(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<line x1='12' y1='19' x2='12' y2='5'/>"
            "<polyline points='5 12 12 5 19 12'/>"
            "</svg>")

def arrow_down(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<line x1='12' y1='5' x2='12' y2='19'/>"
            "<polyline points='19 12 12 19 5 12'/>"
            "</svg>")

def arrow_right(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<line x1='5' y1='12' x2='19' y2='12'/>"
            "<polyline points='12 5 19 12 12 19'/>"
            "</svg>")

def log_out(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4'/>"
            "<polyline points='16 17 21 12 16 7'/>"
            "<line x1='21' y1='12' x2='9' y2='12'/>"
            "</svg>")

def bell(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9'/>"
            "<path d='M13.73 21a2 2 0 0 1-3.46 0'/>"
            "</svg>")

def home(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/>"
            "<polyline points='9 22 9 12 15 12 15 22'/>"
            "</svg>")

def info_icon(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<circle cx='12' cy='12' r='10'/>"
            "<line x1='12' y1='16' x2='12' y2='12'/>"
            "<line x1='12' y1='8' x2='12.01' y2='8'/>"
            "</svg>")

def eye(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z'/>"
            "<circle cx='12' cy='12' r='3'/>"
            "</svg>")

def lock(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<rect x='3' y='11' width='18' height='11' rx='2' ry='2'/>"
            "<path d='M7 11V7a5 5 0 0 1 10 0v4'/>"
            "</svg>")

def user(size="m"):
    a = {"s": _S, "m": _M, "l": _L, "xl": _XL}[size]
    return (f"<svg {a} viewBox='0 0 24 24'>"
            "<path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/>"
            "<circle cx='12' cy='7' r='4'/>"
            "</svg>")

# ── Sidebar icon map (for navigation labels) ───────────────────────
NAV_ICONS = {
    "Vue d'ensemble": "home",
    "Machines": "gear",
    "Production": "clipboard_list",
    "Qualite": "target",
    "Inventaire": "package_icon",
    "Outillage": "wrench",
    "Maintenance": "history",
    "Sensors": "activity",
    "ML Predictions": "bot",
}

ALL_ICONS = {name: obj for name, obj in globals().items()
             if callable(obj) and not name.startswith("_") and name not in ("NAV_ICONS", "ALL_ICONS")}


def icon(name: str, size: str = "m") -> str:
    """Return SVG markup for a named icon at given size."""
    fn = ALL_ICONS.get(name)
    if fn:
        return fn(size)
    return ""


# ── Logo ───────────────────────────────────────────────────────────
def logo_full(size: str = "m"):
    sz = {"s": "120", "m": "160", "l": "200"}.get(size, "160")
    h = str(int(int(sz) * 0.35))
    return f'''<svg width="{sz}" height="{h}" viewBox="0 0 {sz} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B2545"/>
      <stop offset="100%" stop-color="#5B7B9A"/>
    </linearGradient>
  </defs>
  <g transform="translate(0,{int(int(h)*0.08)})">
    <path d="M{int(int(sz)*0.045)} {int(int(h)*0.82)} L{int(int(sz)*0.115)} {int(int(h)*0.12)} L{int(int(sz)*0.185)} {int(int(h)*0.82)}"
          stroke="url(#logoGrad)" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M{int(int(sz)*0.185)} {int(int(h)*0.82)} L{int(int(sz)*0.185)} {int(int(h)*0.82)}
          M{int(int(sz)*0.185)} {int(int(h)*0.55)} L{int(int(sz)*0.185)} {int(int(h)*0.55)}"
          stroke="none"/>
    <line x1="{int(int(sz)*0.065)}" y1="{int(int(h)*0.55)}" x2="{int(int(sz)*0.155)}" y2="{int(int(h)*0.55)}"
          stroke="url(#logoGrad)" stroke-width="2" stroke-linecap="round"/>
    <circle cx="{int(int(sz)*0.115)}" cy="{int(int(h)*0.55)}" r="{max(2,int(int(sz)*0.012))}" fill="#5B7B9A"/>
    <path d="M{int(int(sz)*0.185)} {int(int(h)*0.2)} L{int(int(sz)*0.205)} {int(int(h)*0.15)} L{int(int(sz)*0.205)} {int(int(h)*0.25)} Z"
          fill="#5B7B9A" opacity="0.6"/>
    <path d="M{int(int(sz)*0.185)} {int(int(h)*0.35)} L{int(int(sz)*0.21)} {int(int(h)*0.28)} L{int(int(sz)*0.21)} {int(int(h)*0.42)} Z"
          fill="#5B7B9A" opacity="0.4"/>
    <path d="M{int(int(sz)*0.185)} {int(int(h)*0.55)} L{int(int(sz)*0.215)} {int(int(h)*0.46)} L{int(int(sz)*0.215)} {int(int(h)*0.64)} Z"
          fill="#5B7B9A" opacity="0.25"/>
  </g>
  <text x="{int(int(sz)*0.25)}" y="{int(int(h)*0.52)}"
        font-family="system-ui,-apple-system,sans-serif" font-size="{int(int(sz)*0.145)}" font-weight="800"
        fill="#0B2545" letter-spacing="-0.03">{'A' if size=='s' else 'AMIP'}</text>
  <text x="{int(int(sz)*0.25)}" y="{int(int(h)*0.78)}"
        font-family="system-ui,-apple-system,sans-serif" font-size="{int(int(sz)*0.045)}" font-weight="600"
        fill="#5A6872" letter-spacing="0.12">{'' if size=='s' else 'ADVANCED MANUFACTURING INTELLIGENCE'}</text>
</svg>'''


def logo_icon(size: str = "m"):
    sz = {"s": "28", "m": "36", "l": "48", "xl": "64"}.get(size, "36")
    return f'''<svg width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoIconGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B2545"/>
      <stop offset="100%" stop-color="#5B7B9A"/>
    </linearGradient>
  </defs>
  <rect width="{sz}" height="{sz}" rx="{int(int(sz)*0.22)}" fill="url(#logoIconGrad)"/>
  <path d="M{int(int(sz)*0.3)} {int(int(sz)*0.78)} L{int(int(sz)*0.5)} {int(int(sz)*0.22)} L{int(int(sz)*0.7)} {int(int(sz)*0.78)}"
        stroke="white" stroke-width="{max(1.5,int(int(sz)*0.05))}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="{int(int(sz)*0.37)}" y1="{int(int(sz)*0.56)}" x2="{int(int(sz)*0.63)}" y2="{int(int(sz)*0.56)}"
        stroke="white" stroke-width="{max(1.2,int(int(sz)*0.04))}" stroke-linecap="round"/>
  <circle cx="{int(int(sz)*0.5)}" cy="{int(int(sz)*0.56)}" r="{max(1.2,int(int(sz)*0.035))}" fill="white"/>
  <path d="M{int(int(sz)*0.7)} {int(int(sz)*0.3)} L{int(int(sz)*0.76)} {int(int(sz)*0.22)} L{int(int(sz)*0.76)} {int(int(sz)*0.38)} Z"
        fill="white" opacity="0.5"/>
  <path d="M{int(int(sz)*0.7)} {int(int(sz)*0.46)} L{int(int(sz)*0.78)} {int(int(sz)*0.36)} L{int(int(sz)*0.78)} {int(int(sz)*0.56)} Z"
        fill="white" opacity="0.3"/>
</svg>'''


def icon_html(name: str, size: str = "m", color: str = None, class_name: str = "") -> str:
    """Return a styled icon div suitable for embedding in HTML."""
    svg = icon(name, size)
    c = f"color:{color};" if color else ""
    cn = f" class='{class_name}'" if class_name else ""
    return f"<span{cn} style='display:inline-flex;align-items:center;justify-content:center;{c}'>{svg}</span>"

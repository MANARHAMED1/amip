import datetime
import streamlit as st
from dashboard.api_client import get
from dashboard.icons import (factory, gear, clipboard_list, target, package_icon,
                               wrench, history, bell, log_out, user, search,
                               alert_triangle, alert_circle, icon, icon_html, logo_icon)

# Page name -> (svg function, label)
NAV_ITEMS = [
    ("Vue d'ensemble", "home"),
    ("Machines", "gear"),
    ("Production", "clipboard_list"),
    ("Qualite", "target"),
    ("Inventaire", "package_icon"),
    ("Outillage", "wrench"),
    ("Maintenance", "history"),
]

NAV_LABELS = [item[0] for item in NAV_ITEMS]
NAV_ICON_NAMES = [item[1] for item in NAV_ITEMS]


def render_sidebar():
    with st.sidebar:
        nav_icons_html = ""
        for name, iname in NAV_ITEMS:
            svg = icon(iname, "s")
            nav_icons_html += f'<span style="margin-right:4px">{svg}</span>'

        st.html(f"""
        <div style="padding:4px 0 20px 0;margin-bottom:16px;text-align:center">
            {logo_icon("m")}
            <div style="color:white;font-size:14px;font-weight:800;letter-spacing:-0.02em;margin-top:8px">AMIP</div>
            <div style="color:#8A95A0;font-size:8px;letter-spacing:1.5px;font-weight:500;text-transform:uppercase">MFG Intelligence</div>
        </div>
        """)

        # Navigation with hidden icons using native radio
        page = st.radio("Navigation", NAV_LABELS, label_visibility="collapsed")

        st.html('<div style="border-top:1px solid rgba(255,255,255,0.06);margin:14px 0"></div>')

        # User section
        st.html(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;
                    background:rgba(255,255,255,0.04);border-radius:8px;margin-bottom:12px">
            <div style="width:32px;height:32px;background:#5B7B9A;border-radius:6px;
                        display:flex;align-items:center;justify-content:center;color:white;
                        font-size:12px;font-weight:700">
                {st.session_state.get('full_name', st.session_state.get('username','A'))[0].upper()}
            </div>
            <div>
                <div style="color:white;font-size:12px;font-weight:600">{st.session_state.get('full_name', 'User')}</div>
                <div style="color:#8A95A0;font-size:10px">{st.session_state.get('user_role', 'operator').title()}</div>
            </div>
        </div>
        """)

        # Alerts in sidebar
        _render_alerts()

        st.html('<div style="border-top:1px solid rgba(255,255,255,0.06);margin:14px 0"></div>')

        if st.button("Sign Out", key="logout_btn", width="stretch"):
            st.session_state.authenticated = False
            st.session_state.jwt_token = None
            st.session_state.username = None
            st.session_state.full_name = None
            st.session_state.user_role = None
            st.rerun()

    return page


def render_global_filters():
    st.html(f"""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;padding:0 4px">
        <span style="color:#64748B">{icon("filter_icon", "s")}</span>
        <span style="color:#64748B;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em">Filtres globaux</span>
    </div>
    """)

    cols = st.columns([2, 2, 2, 2])
    with cols[0]:
        today = datetime.date.today()
        ds = st.date_input("Du", value=st.session_state.get("date_start", today - datetime.timedelta(days=90)),
                           key="date_start_input")
        st.session_state["date_start"] = ds
    with cols[1]:
        de = st.date_input("Au", value=st.session_state.get("date_end", today),
                           key="date_end_input")
        st.session_state["date_end"] = de
    with cols[2]:
        machines_data = get("/machine/list") or []
        if isinstance(machines_data, list) and machines_data:
            codes = ["Toutes"] + [m["code"] for m in machines_data]
        else:
            codes = ["Toutes"]
        st.selectbox("Machine", codes, key="machine_filter")
    with cols[3]:
        st.selectbox("Secteur", ["Tous", "T01", "T02", "T03"], key="sector_filter")


def render_critical_alerts():
    """Render a professional alert panel at the top of the dashboard."""
    alerts = get("/executive/alerts")
    if not alerts or not isinstance(alerts, list) or not alerts:
        return

    critical = [a for a in alerts if a.get("type") == "CRITICAL"]
    warning = [a for a in alerts if a.get("type") == "WARNING"]

    if not critical and not warning:
        return

    n_crit = len(critical)
    n_warn = len(warning)

    items = ""

    crit_icon = '<span style="color:#C62828;font-size:13px;font-weight:700;flex-shrink:0">!</span>'
    warn_icon = '<span style="color:#ED6C02;font-size:13px;font-weight:700;flex-shrink:0">!</span>'

    for a in critical:
        msg = a.get("message", "")
        detail = a.get("detail", "")
        detail_html = f'<div style="color:#5A6872;font-size:11px;margin-top:1px">{detail}</div>' if detail else ""
        items += (
            '<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;margin-bottom:5px;'
            'background:#FDF6F6;border:1px solid #C6282820;border-left:3px solid #C62828;border-radius:6px;'
            'animation:alertPulse 2.5s ease-in-out infinite">'
            f'{crit_icon}'
            '<div style="flex:1;min-width:0">'
            f'<div style="color:#1C1E21;font-size:12px;font-weight:600">{msg}</div>'
            f'{detail_html}'
            '</div></div>'
        )

    for a in warning:
        msg = a.get("message", "")
        detail = a.get("detail", "")
        detail_html = f'<div style="color:#5A6872;font-size:11px;margin-top:1px">{detail}</div>' if detail else ""
        items += (
            '<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;margin-bottom:4px;'
            'background:#FFFBF5;border:1px solid #ED6C0220;border-left:3px solid #ED6C02;border-radius:6px">'
            f'{warn_icon}'
            '<div style="flex:1;min-width:0">'
            f'<div style="color:#1C1E21;font-size:12px;font-weight:600">{msg}</div>'
            f'{detail_html}'
            '</div></div>'
        )

    badge_crit = f'<span style="background:#C6282818;color:#C62828;font-size:11px;font-weight:600;padding:2px 10px;border-radius:10px;border:1px solid #C6282830">{n_crit} Critical</span>' if n_crit else ""
    badge_warn = f'<span style="background:#ED6C0218;color:#ED6C02;font-size:11px;font-weight:600;padding:2px 10px;border-radius:10px;border:1px solid #ED6C0230">{n_warn} Warning</span>' if n_warn else ""

    html = (
        '<div style="background:#FFFFFF;border:1px solid #E2E5E9;border-radius:10px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,0.04)">'
        '<div style="display:flex;align-items:center;gap:10px;padding:14px 18px;border-bottom:1px solid #E2E5E9">'
        f'<span style="font-size:15px;font-weight:700;color:#1C1E21;font-family:system-ui,sans-serif">Alerts</span>'
        f'{badge_crit}{badge_warn}'
        '</div>'
        '<div style="max-height:420px;overflow-y:auto;padding:10px 14px">'
        f'{items}'
        '</div></div>'
    )

    st.html(html)


def _render_alerts():
    st.html('<div style="color:#94A3B8;font-size:11px;font-weight:600;margin:8px 0 10px;letter-spacing:0.05em">STOCK</div>')
    alerts = get("/inventory/alerts")
    if not alerts or not isinstance(alerts, list):
        st.info("OK")
        return
    critical = [a for a in alerts if a.get("statut") == "CRITIQUE"]
    low = [a for a in alerts if a.get("statut") == "BAS"]
    if critical:
        st.error(f"{len(critical)} Critical")
        for a in critical[:3]:
            code = a.get("code", "")
            desc = a.get("designation", "")[:25]
            stock = a.get("quantite_stock", 0)
            seuil = a.get("seuil_alerte", 0)
            st.caption(f"{code} {desc} ({stock}/{seuil})")
    if low:
        st.warning(f"{len(low)} Low")
        for a in low[:3]:
            code = a.get("code", "")
            desc = a.get("designation", "")[:25]
            stock = a.get("quantite_stock", 0)
            seuil = a.get("seuil_alerte", 0)
            st.caption(f"{code} {desc} ({stock}/{seuil})")
    if not critical and not low:
        st.success("OK")

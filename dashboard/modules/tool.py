import streamlit as st
import pandas as pd
from dashboard.api_client import get
from dashboard.charts import (kpi_card, bar_chart, progress_bar, status_badge, THEME,
                               section_header)
from dashboard.icons import icon, icon_html


def render():
    st.subheader("Gestion Outillage")

    tools = get("/tool/list")
    if not tools or not isinstance(tools, list):
        st.error("Donnees outillage indisponibles")
        return

    critical = sum(1 for t in tools if t.get("indicateur_remplacement") == "CRITICAL")
    warning = sum(1 for t in tools if t.get("indicateur_remplacement") == "WARNING")
    available = sum(1 for t in tools if t.get("disponible"))

    st.html(section_header("Vue d'ensemble", "wrench", "Etat du parc outillage"))
    st.html(f"""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:24px">
        {kpi_card("Total outils", len(tools), icon_name="wrench")}
        {kpi_card("Disponibles", available, icon_name="check_circle")}
        {kpi_card("Critiques", critical, icon_name="alert_circle")}
        {kpi_card("Avertissement", warning, icon_name="alert_triangle")}
        {kpi_card("Taux dispo", round(available / len(tools) * 100, 1) if tools else 0, unit="%", icon_name="chart_bar")}
    </div>
    """)

    if "selected_tool" in st.session_state:
        _render_detail(st.session_state.selected_tool)
        if st.button("Retour a la liste", key="back_tool"):
            del st.session_state.selected_tool
            st.rerun()
        return

    st.html(section_header("Recherche", "search"))
    search = st.text_input("Rechercher un outil...", placeholder="Code, designation, type...")
    filtered = tools
    if search:
        filtered = [t for t in tools if search.lower() in t.get("code", "").lower()
                    or search.lower() in t.get("designation", "").lower()]

    df = pd.DataFrame(filtered)
    if not df.empty:
        st.html(section_header("Liste des outils", "list"))
        for _, row in df.iterrows():
            pct = row.get("pct_usure", 0) or 0
            indicator = row.get("indicateur_remplacement", "OK")
            if indicator == "OK":
                color = THEME["green"]
            elif indicator == "WARNING":
                color = THEME["amber"]
            else:
                color = THEME["red"]

            stock_info = row.get("stock", 0)
            qty = stock_info if isinstance(stock_info, (int, float)) else (stock_info.get("quantite_stock", 0) if isinstance(stock_info, dict) else 0)
            st.html(f"""
            <div style="background:white;border:1px solid #E2E8F0;border-radius:8px;padding:12px 16px;margin-bottom:5px;
                        box-shadow:0 1px 2px rgba(0,0,0,0.03);border-left:3px solid {color};
                        transition:all 0.2s cubic-bezier(0.4,0,0.2,1)">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div style="display:flex;align-items:center;gap:10px">
                        <div style="width:30px;height:30px;background:{color}10;border-radius:8px;display:flex;align-items:center;justify-content:center;color:{color}">
                            {icon('wrench', 's')}
                        </div>
                        <div>
                            <span style="color:#0B2545;font-weight:700;font-family:'Consolas','Courier New',monospace;font-size:12px">{row.get('code','')}</span>
                            <span style="color:#1E293B;font-size:12px;margin-left:8px">{row.get('designation','')}</span>
                            <span style="color:#94A3B8;font-size:11px;margin-left:8px">{row.get('type_outil','')} - {row.get('diametre','')}mm</span>
                        </div>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px">
                        <span style="color:#64748B;font-size:11px;font-family:'Consolas','Courier New',monospace">Stock: {qty}</span>
                        <span style="color:{color};font-size:11px;font-weight:700">{indicator}</span>
                    </div>
                </div>
                <div style="margin-top:8px">
                    <div style="display:flex;justify-content:space-between;font-size:10px;color:#64748B;margin-bottom:3px">
                        <span>Usure: {row.get('usure_actuelle',0)}/{row.get('duree_vie_totale',0)}</span>
                        <span style="color:{color};font-weight:700;font-family:'Consolas','Courier New',monospace">{pct:.0f}%</span>
                    </div>
                    {progress_bar(pct, color=color)}
                </div>
            </div>
            """)
            if st.button(f"Details {row['code']}", key=f"tool_{row['code']}", width="stretch"):
                st.session_state.selected_tool = row["code"]
                st.rerun()


def _render_detail(tool_code):
    detail = get(f"/tool/{tool_code}")
    if not detail or "error" in (detail or {}):
        st.error("Outil introuvable")
        return

    t = detail.get("tool", {})
    executions = detail.get("executions", [])
    stats = detail.get("stats", {})

    pct = t.get("pct_usure", 0) or 0
    color = THEME["green"] if pct < 50 else THEME["amber"] if pct < 80 else THEME["red"]

    st.html(section_header(f"Outil {tool_code}", "wrench", t.get('designation','')))
    st.html(f"""
    <div style="background:white;border:1px solid #E2E8F0;border-radius:12px;padding:18px 22px;margin-bottom:20px;
                box-shadow:0 1px 3px rgba(0,0,0,0.04)">
        <div style="display:flex;align-items:center;gap:14px">
            <div style="width:40px;height:40px;background:{color}10;border-radius:10px;display:flex;align-items:center;justify-content:center;color:{color}">
                {icon('wrench', 'm')}
            </div>
            <div>
                <span style="color:#0B2545;font-size:18px;font-weight:800;font-family:'Consolas','Courier New',monospace">{tool_code}</span>
                <span style="color:#1E293B;font-size:13px;margin-left:10px">{t.get('designation','')}</span>
            </div>
            <span style="color:#94A3B8;font-size:11px;margin-left:8px">{t.get('type_outil','')} - {t.get('matiere_outil','')} - {t.get('diametre','')}mm</span>
        </div>
    </div>
    """)

    st.html(section_header("Details", "info"))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.html(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;padding:16px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px">
                <span style="color:{color}">{icon('chart_bar', 's')}</span>
                <span style="color:#94A3B8;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;font-weight:600">Usure</span>
            </div>
            <div style="color:{color};font-size:28px;font-weight:800;font-family:'Consolas','Courier New',monospace">{pct:.0f}%</div>
            <div style="margin-top:10px">{progress_bar(pct, color=color)}</div>
            <div style="color:#94A3B8;font-size:10px;margin-top:8px">{t.get('usure_actuelle',0)} / {t.get('duree_vie_totale',0)} cycles</div>
        </div>
        """)
    with col2:
        st.html(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;padding:16px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px">
                <span style="color:#0B2545">{icon('coins', 's')}</span>
                <span style="color:#94A3B8;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;font-weight:600">Couts</span>
            </div>
            <div style="color:#1E293B;font-size:12px">Achat: <b>{t.get('cout_achat',0):.2f}</b> MAD</div>
            <div style="color:#1E293B;font-size:12px">Remplacement: <b>{t.get('cout_remplacement',0):.2f}</b> MAD</div>
            <div style="color:#1E293B;font-size:12px">Vie restante: <b>{t.get('duree_vie_restante',0)}</b> cycles</div>
        </div>
        """)
    with col3:
        st.html(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;padding:16px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px">
                <span style="color:#5B7B9A">{icon('chart_bar', 's')}</span>
                <span style="color:#94A3B8;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;font-weight:600">Statistiques</span>
            </div>
            <div style="color:#1E293B;font-size:12px">Utilisations: <b>{stats.get('nb_executions',0)}</b></div>
            <div style="color:#1E293B;font-size:12px">Duree totale: <b>{stats.get('duree_totale',0)}</b> min</div>
            <div style="color:#1E293B;font-size:12px">Usure moy.: <b>{stats.get('usure_moyenne_par_exec',0)}</b></div>
        </div>
        """)

    if executions:
        st.html(section_header("Historique d'utilisation", "history"))
        st.dataframe(pd.DataFrame(executions), width="stretch", hide_index=True)

import streamlit as st
import pandas as pd
from dashboard.api_client import get, get_with_filters
from dashboard.charts import (kpi_card, gauge_chart, bar_chart, line_chart,
                               pie_chart, machine_card_html, THEME, status_badge,
                               progress_bar, section_header)
from dashboard.icons import icon, icon_html


def render():
    kpi = get_with_filters("/executive/kpi")
    if not kpi:
        st.error("Donnees KPI indisponibles")
        return

    oee_data = kpi.get("oee", {})
    machines_count = kpi.get("machines", {})
    of_data = kpi.get("ordres_fabrication", {})
    retards_raw = kpi.get("retards", {})
    retards = retards_raw.get("retard", 0) if isinstance(retards_raw, dict) else (retards_raw or 0)

    # ── Section: KPI Overview ──
    st.html(section_header("Vue d'ensemble", "home", "Indicateurs cles de performance"))
    st.html(f"""
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:24px">
        {kpi_card("OEE Global", oee_data.get("oee_global", 0), icon_name="chart_bar", subtitle="Disponibilite x Performance x Qualite")}
        {kpi_card("Taux Rebut", oee_data.get("taux_rebut", 0), unit="%", icon_name="target")}
        {kpi_card("Machines en marche", machines_count.get("running", 0), icon_name="gear",
                  subtitle=f"Arretees: {machines_count.get('stopped',0)} | Maintenance: {machines_count.get('maintenance',0)}")}
        {kpi_card("OF actifs", of_data.get("en_cours", 0), icon_name="clipboard_list",
                  subtitle=f"En attente: {of_data.get('en_attente',0)} | Termines: {of_data.get('termine',0)}")}
        {kpi_card("Retards", retards, icon_name="clock",
                  subtitle="Ordres en retard")}
        {kpi_card("Qualite", oee_data.get("qualite", 0), unit="%", icon_name="shield")}
    </div>
    """)

    # ── Section: Performance ──
    st.html(section_header("Performance Production", "chart_bar", "OEE par machine et production vs plan"))
    col1, col2 = st.columns([2, 1])

    with col1:
        oee_by_machine = get_with_filters("/executive/oee-by-machine")
        if oee_by_machine and isinstance(oee_by_machine, list) and len(oee_by_machine) > 0:
            df = pd.DataFrame(oee_by_machine)
            df = df.sort_values("oee", ascending=True)
            fig = bar_chart(df, x="code", y="oee", title="")
            if fig:
                fig.update_traces(
                    marker_color=[THEME["green"] if v >= 70 else THEME["amber"] if v >= 50 else THEME["red"]
                                  for v in df["oee"]],
                    showlegend=False)
                st.plotly_chart(fig, width="stretch")

    with col2:
        vs_plan = get_with_filters("/executive/production-vs-plan")
        if vs_plan and isinstance(vs_plan, list) and len(vs_plan) > 0:
            df = pd.DataFrame(vs_plan)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df_recent = df.tail(30)
                fig = line_chart(df_recent, x="date", y=["planifie", "reel"])
                if fig:
                    st.plotly_chart(fig, width="stretch")

    # ── Section: Machines & Qualite ──
    st.html(section_header("Machines & Qualite", "gear", "Etat des machines et analyse des rebuts"))
    col3, col4 = st.columns(2)

    with col3:
        machines = get("/executive/machine-status")
        if machines and isinstance(machines, list):
            html = ""
            for m in machines:
                html += machine_card_html(m)
            st.html(html)

    with col4:
        scrap = get_with_filters("/executive/scrap-by-family")
        if scrap and isinstance(scrap, list) and len(scrap) > 0:
            df = pd.DataFrame(scrap)
            fig = pie_chart(df, names="famille", values="nb_rebut")
            if fig:
                st.plotly_chart(fig, width="stretch")

        trend = get_with_filters("/executive/production-trend")
        if trend and isinstance(trend, list) and len(trend) > 0:
            df = pd.DataFrame(trend)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df_recent = df.tail(30)
                fig = line_chart(df_recent, x="date", y=["produites", "rebuts"])
                if fig:
                    st.plotly_chart(fig, width="stretch")

    # ── Section: Ordres de Fabrication Actifs ──
    st.html(section_header("Ordres de Fabrication Actifs", "clipboard_list", "Suivi des OF en cours"))
    active = get_with_filters("/executive/active-orders")
    if active and isinstance(active, list) and len(active) > 0:
        df = pd.DataFrame(active)
        if "avancement_pct" in df.columns:
            df = df.sort_values("avancement_pct", ascending=False)
        for _, row in df.iterrows():
            pct = row.get("avancement_pct", 0) or 0
            statut = row.get("statut", "")
            sc = THEME["green"] if statut == "EN_COURS" else THEME["primary"] if statut == "TERMINE" else THEME["amber"] if statut in ("EN_ATTENTE", "EN_RETARD") else THEME["text_dim"]
            retard = row.get("retard_jours", 0) or 0
            retard_html = f'<span style="color:#C62828;font-size:11px;font-weight:700;margin-left:8px">+{retard}j</span>' if retard > 0 else ''
            st.html(f"""
            <div class="card-lift" style="background:white;border:1px solid #E2E8F0;border-radius:8px;padding:12px 16px;margin-bottom:5px;
                        box-shadow:0 1px 2px rgba(0,0,0,0.03);border-left:3px solid {sc};
                        transition:all 0.2s cubic-bezier(0.4,0,0.2,1)">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div style="display:flex;align-items:center;gap:12px">
                        <span style="color:#0B2545;font-weight:700;font-family:'Consolas','Courier New',monospace;font-size:13px">{row.get('numero_of','')}</span>
                        <span style="color:#1E293B;font-size:12px">{row.get('piece_ref','')} - {row.get('piece_nom','')[:40]}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:12px">
                        <span style="color:#64748B;font-size:11px;font-family:'Consolas','Courier New',monospace">{row.get('quantite_produite',0)}/{row.get('quantite_demandee',0)}</span>
                        {status_badge(statut)}
                        {retard_html}
                    </div>
                </div>
                <div style="margin-top:8px">{progress_bar(pct)}</div>
            </div>
            """)
    else:
        st.info("Aucun OF actif")

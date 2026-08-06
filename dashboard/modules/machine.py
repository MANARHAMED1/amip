import streamlit as st
import pandas as pd
from dashboard.api_client import get, get_with_filters
from dashboard.charts import (kpi_card, gauge_chart, bar_chart, line_chart,
                               multi_line_chart, gantt_timeline, status_badge, THEME,
                               progress_bar, section_header)
from dashboard.icons import icon, icon_html


def render():
    st.subheader("Analyse Machine")

    machines = get("/machine/list")
    if not machines or not isinstance(machines, list) or not machines:
        st.error("Aucune machine trouvee")
        return

    codes = [m["code"] for m in machines]
    selected = st.selectbox("Selectionner une machine", codes)

    info = get(f"/machine/{selected}")
    if not info or "error" in (info or {}):
        st.error(info.get("error", "Machine introuvable") if info else "Erreur de chargement")
        return

    machine_info = info.get("machine", {})
    operateur = info.get("operateur")
    outil = info.get("outil_actuel")
    statut = machine_info.get("statut", "UNKNOWN")

    if statut == "RUNNING":
        color = THEME["green"]
    elif statut in ("STOPPED", "BROKEN"):
        color = THEME["red"]
    else:
        color = THEME["amber"]

    # ── Machine Header Card ──
    badge = status_badge(statut)
    st.html(f"""
    <div class="card-lift" style="display:flex;align-items:center;gap:16px;margin-bottom:20px;padding:18px 22px;
                background:white;border:1px solid #E2E8F0;border-radius:12px;
                box-shadow:0 1px 3px rgba(0,0,0,0.04);border-left:4px solid {color}">
        <div style="width:44px;height:44px;background:{color}10;border-radius:12px;display:flex;align-items:center;
                    justify-content:center;color:{color}">
            {icon('gear', 'm')}
        </div>
        <div>
            <div style="font-size:20px;font-weight:800;color:#1E293B;font-family:'Consolas','Courier New',monospace">{machine_info.get('code','')}</div>
            <div style="color:#64748B;font-size:12px;margin-top:2px">{machine_info.get('nom','')}</div>
        </div>
        <div style="margin-left:12px">{badge}</div>
        <div style="margin-left:auto;display:flex;gap:14px;color:#94A3B8;font-size:11px">
            <span>{machine_info.get('type','')}</span>
            <span>{machine_info.get('marque','')} {machine_info.get('modele','')}</span>
            <span>{machine_info.get('controller','')}</span>
        </div>
    </div>
    """)

    if operateur:
        st.html(f"""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 14px;background:#F1F5F9;border-radius:8px;margin-bottom:16px;font-size:12px">
            <span style="color:#64748B">{icon('user', 's')}</span>
            <span style="color:#1E293B">Operateur: <b>{operateur.get('prenom','')} {operateur.get('nom','')}</b> ({operateur.get('matricule','')})</span>
        </div>
        """)

    # ── Performance KPIs ──
    st.html(section_header("Performance", "chart_bar", "Indicateurs de performance machine"))
    perf = get(f"/machine/{selected}/performance")
    if perf:
        st.html(f"""
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:24px">
            {kpi_card("Disponibilite", round(perf.get("disponibilite", 0) * 100, 1), unit="%", icon_name="zap")}
            {kpi_card("Performance", round(perf.get("performance", 0) * 100, 1), unit="%", icon_name="chart_bar")}
            {kpi_card("Qualite", round(perf.get("qualite", 0) * 100, 1), unit="%", icon_name="shield")}
            {kpi_card("OEE", round(perf.get("oee", 0) * 100, 1), unit="%", icon_name="chart_bar")}
            {kpi_card("Pieces produites", perf.get("total_produites", 0), icon_name="target")}
        </div>
        """)

    # ── OEE History + Sensors ──
    st.html(section_header("Historique & Capteurs", "activity", "OEE dans le temps et donnees capteurs actuelles"))
    col1, col2 = st.columns(2)
    with col1:
        oee_hist = get(f"/machine/{selected}/oee-history")
        if oee_hist and isinstance(oee_hist, list) and len(oee_hist) > 0:
            df = pd.DataFrame(oee_hist)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("date")
                fig = multi_line_chart(df, x="date", y_list=["oee", "disponibilite", "performance", "qualite"])
                if fig:
                    fig.update_layout(legend=dict(orientation="h", y=-0.18))
                    st.plotly_chart(fig, width="stretch")

    with col2:
        sensors_data = get(f"/machine/{selected}/sensors")
        if sensors_data:
            current = sensors_data.get("current", {})
            stats = sensors_data.get("stats", {})
            if current:
                t = current.get("temperature", 0) or 0
                v = current.get("vibration", 0) or 0
                anomaly = min(100, (t / 80 * 40) + (v / 4.5 * 60))
                st.html(f"""
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:10px">
                    {kpi_card("Temperature", round(t, 1), unit="C", icon_name="thermometer")}
                    {kpi_card("Vibration", round(v, 2), unit="mm/s", icon_name="activity")}
                    {kpi_card("Anomalie", round(anomaly, 0), unit="%", icon_name="alert_triangle")}
                </div>
                """)
            if stats:
                st.html(f"""
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">
                    {kpi_card("RPM moyen", round(stats.get("rpm_moy", 0), 0), icon_name="refresh")}
                    {kpi_card("Puissance max", round(stats.get("puissance_max", 0), 1), unit="kW", icon_name="zap")}
                    {kpi_card("Nb alertes", stats.get("alertes_temp", 0) + stats.get("alertes_vibration", 0), icon_name="bell")}
                </div>
                """)

    # ── Timeline + Tooling ──
    st.html(section_header("Planning & Outillage", "calendar", "Phases planifiees et etat de l'outillage"))
    col3, col4 = st.columns(2)
    with col3:
        timeline = get(f"/machine/{selected}/phases-timeline")
        if timeline and isinstance(timeline, list) and len(timeline) > 0:
            df = pd.DataFrame(timeline)
            fig = gantt_timeline(df)
            if fig:
                st.plotly_chart(fig, width="stretch")

    with col4:
        if outil:
            pct = outil.get("pct_usure", 0) or 0
            tc = THEME["green"] if pct < 50 else THEME["amber"] if pct < 80 else THEME["red"]
            st.html(f"""
            <div class="card-lift" style="background:white;border:1px solid #E2E8F0;border-radius:10px;padding:16px;
                        box-shadow:0 1px 2px rgba(0,0,0,0.04)">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
                    <div style="width:32px;height:32px;background:{tc}10;border-radius:8px;display:flex;align-items:center;justify-content:center;color:{tc}">
                        {icon('wrench', 's')}
                    </div>
                    <div>
                        <div style="color:#1E293B;font-weight:700;font-size:13px;font-family:'Consolas','Courier New',monospace">{outil.get('code','')}</div>
                        <div style="color:#64748B;font-size:11px">{outil.get('designation','')}</div>
                    </div>
                </div>
                <div style="color:#94A3B8;font-size:11px;margin-bottom:10px">{outil.get('type_outil','')} - Diametre: {outil.get('diametre','')}mm</div>
                <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:5px">
                    <span style="color:#64748B">Usure</span>
                    <span style="color:{tc};font-weight:700;font-family:'Consolas','Courier New',monospace">{pct:.0f}%</span>
                </div>
                {progress_bar(pct, color=tc)}
                <div style="color:#94A3B8;font-size:11px;margin-top:6px">{outil.get('usure_actuelle',0)} / {outil.get('duree_vie_totale',0)} cycles</div>
            </div>
            """)

        st.html(section_header("Maintenance Recente", "history"))
        maint = get(f"/machine/{selected}/maintenance")
        if maint and isinstance(maint, list) and len(maint) > 0:
            df = pd.DataFrame(maint[:5])
            st.dataframe(df, width="stretch", hide_index=True)

        m_kpi = get(f"/machine/{selected}/maintenance-kpi")
        if m_kpi:
            mtbf_mttr = m_kpi.get("mtbf_mttr", {})
            if mtbf_mttr:
                st.html(f"""
                <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px">
                    {kpi_card("MTBF", round(mtbf_mttr.get("mtbf_heures", 0), 1), unit="h", icon_name="timer")}
                    {kpi_card("MTTR", round(mtbf_mttr.get("mttr_heures", 0), 1), unit="h", icon_name="history")}
                </div>
                """)

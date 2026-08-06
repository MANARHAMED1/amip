import streamlit as st
import pandas as pd
from dashboard.api_client import get, get_with_filters
from dashboard.charts import (kpi_card, gauge_chart, bar_chart, line_chart,
                               pie_chart, THEME, section_header)
from dashboard.icons import icon, icon_html


def render():
    st.subheader("Maintenance")

    m_kpi = get_with_filters("/maintenance/kpi")
    if not m_kpi:
        st.error("Donnees maintenance indisponibles")
        return

    stats = m_kpi.get("stats", {})
    by_type = m_kpi.get("by_type", [])

    duree_tot = stats.get("duree_totale_min", 0) or 0
    nb_corr = stats.get("nb_corrective", 0) or 0
    nb_prev = stats.get("nb_preventive", 0) or 0
    nb_total = stats.get("nb_interventions", 0) or 0

    mtbf = round((duree_tot / 60) / max(nb_corr, 1), 1) if nb_corr > 0 else 0
    mttr = round((stats.get("duree_moyenne_min", 0) or 0) / 60, 1)
    dispo = round(mtbf / max(mtbf + mttr, 0.1) * 100, 1)

    st.html(section_header("Vue d'ensemble", "wrench", "Indicateurs de maintenance"))
    st.html(f"""
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:24px">
        {kpi_card("Interventions", nb_total, icon_name="wrench")}
        {kpi_card("Correctives", nb_corr, icon_name="alert_circle")}
        {kpi_card("Preventives", nb_prev, icon_name="shield")}
        {kpi_card("MTBF", mtbf, unit="h", icon_name="timer")}
        {kpi_card("MTTR", mttr, unit="h", icon_name="history")}
        {kpi_card("Disponibilite", dispo, unit="%", icon_name="zap")}
    </div>
    """)

    st.html(section_header("Repartition", "pie_chart"))
    col1, col2 = st.columns(2)
    with col1:
        fig = gauge_chart(dispo, "Disponibilite", thresholds={"green": 90, "orange": 80})
        st.plotly_chart(fig, width="stretch")
    with col2:
        if by_type and isinstance(by_type, list) and len(by_type) > 0:
            df = pd.DataFrame(by_type)
            fig = pie_chart(df, names="type_maintenance", values="nb", title="Repartition par type")
            if fig:
                st.plotly_chart(fig, width="stretch")

    tabs = st.tabs(["Historique", "Evolution couts", "Frequence"])

    with tabs[0]:
        st.html(section_header("Historique des interventions", "history"))
        history = get_with_filters("/maintenance/list")
        if history and isinstance(history, list) and len(history) > 0:
            st.dataframe(pd.DataFrame(history), width="stretch", hide_index=True)

    with tabs[1]:
        st.html(section_header("Couts & Interventions", "trending_up"))
        cost_evo = get_with_filters("/maintenance/cost-evolution")
        if cost_evo and isinstance(cost_evo, list) and len(cost_evo) > 0:
            df = pd.DataFrame(cost_evo)
            fig = bar_chart(df, x="mois", y="cout_mensuel", title="Evolution couts mensuels")
            if fig:
                fig.update_traces(marker_color=THEME["amber"], showlegend=False)
                st.plotly_chart(fig, width="stretch")
            fig2 = line_chart(df, x="mois", y="nb_interventions", title="Nombre d'interventions")
            if fig2:
                st.plotly_chart(fig2, width="stretch")

    with tabs[2]:
        st.html(section_header("Par machine", "gear"))
        history = get_with_filters("/maintenance/list")
        if history and isinstance(history, list) and len(history) > 0:
            df = pd.DataFrame(history)
            if "machine_code" in df.columns:
                mc = df["machine_code"].value_counts().reset_index()
                mc.columns = ["machine_code", "nb_interventions"]
                fig = bar_chart(mc.sort_values("nb_interventions", ascending=True),
                               x="machine_code", y="nb_interventions", title="Interventions par machine", horizontal=True)
                if fig:
                    fig.update_traces(marker_color=THEME["primary"], showlegend=False)
                    st.plotly_chart(fig, width="stretch")

import streamlit as st
import pandas as pd
from dashboard.api_client import get, get_with_filters
from dashboard.charts import (kpi_card, gauge_chart, bar_chart, line_chart,
                               pie_chart, scatter_chart, tolerance_chart, THEME,
                               section_header)
from dashboard.icons import icon, icon_html


def render():
    st.subheader("Controle Qualite")

    kpi = get_with_filters("/quality/kpi")
    if not kpi:
        st.error("Donnees qualite indisponibles")
        return

    conformite = kpi.get("taux_conformite", 0) or 0
    non_conformes = kpi.get("total_non_conformes", 0) or 0

    st.html(section_header("Vue d'ensemble", "target", "Indicateurs qualite"))
    st.html(f"""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:24px">
        {kpi_card("Controles", kpi.get("total_controles", 0), icon_name="search")}
        {kpi_card("Conformes", kpi.get("total_conformes", 0), icon_name="check_circle")}
        {kpi_card("Non conformes", non_conformes, icon_name="x_circle")}
        {kpi_card("Taux conformite", round(conformite * 100, 2) if conformite < 10 else round(conformite, 2), unit="%", icon_name="target")}
        {kpi_card("Ecart moy.", round(kpi.get("ecart_dimension_moyen", 0) or 0, 3), unit="mm", icon_name="ruler")}
    </div>
    """)

    st.html(section_header("Jauges", "gauge"))
    col1, col2 = st.columns(2)
    with col1:
        val_rebut = round((1 - conformite) * 100, 2) if conformite <= 1 else round(100 - conformite, 2)
        fig = gauge_chart(val_rebut, "Taux Rebut", thresholds={"green": 2, "orange": 5})
        st.plotly_chart(fig, width="stretch")
    with col2:
        fig = gauge_chart(conformite if conformite <= 100 else conformite, "Conformite",
                         thresholds={"green": 95, "orange": 90})
        st.plotly_chart(fig, width="stretch")

    tabs = st.tabs(["Causes", "Par machine", "Par operateur", "Par piece", "Par matiere", "Evolution", "Dimensions"])

    with tabs[0]:
        st.html(section_header("Causes de rebut", "alert_triangle"))
        causes = get_with_filters("/quality/causes")
        if causes and isinstance(causes, list) and len(causes) > 0:
            df = pd.DataFrame(causes)
            fig = bar_chart(df, x="categorie", y="nb", color="categorie", title="Causes de rebut", horizontal=True)
            if fig:
                st.plotly_chart(fig, width="stretch")
            st.dataframe(df, width="stretch", hide_index=True)

    with tabs[1]:
        st.html(section_header("Par machine", "gear"))
        by_machine = get_with_filters("/quality/by-machine")
        if by_machine and isinstance(by_machine, list) and len(by_machine) > 0:
            df = pd.DataFrame(by_machine)
            fig = bar_chart(df, x="code", y="taux_rebut", title="Taux rebut par machine")
            if fig:
                fig.update_traces(marker_color=THEME["primary"], showlegend=False)
                st.plotly_chart(fig, width="stretch")

    with tabs[2]:
        st.html(section_header("Par operateur", "user"))
        by_op = get_with_filters("/quality/by-operator")
        if by_op and isinstance(by_op, list) and len(by_op) > 0:
            df = pd.DataFrame(by_op)
            df["nom_complet"] = df["nom"] + " " + df["prenom"]
            fig = bar_chart(df.sort_values("taux_rebut", ascending=True), x="nom_complet", y="taux_rebut",
                           title="Taux rebut par operateur")
            if fig:
                fig.update_traces(marker_color=THEME["amber"], showlegend=False)
                st.plotly_chart(fig, width="stretch")

    with tabs[3]:
        st.html(section_header("Par piece", "box"))
        by_part = get_with_filters("/quality/by-part")
        if by_part and isinstance(by_part, list) and len(by_part) > 0:
            df = pd.DataFrame(by_part)
            st.dataframe(df, width="stretch", hide_index=True)

    with tabs[4]:
        st.html(section_header("Par matiere", "package"))
        by_mat = get_with_filters("/quality/by-material")
        if by_mat and isinstance(by_mat, list) and len(by_mat) > 0:
            df = pd.DataFrame(by_mat)
            st.dataframe(df, width="stretch", hide_index=True)

    with tabs[5]:
        st.html(section_header("Evolution", "trending_up"))
        evolution = get_with_filters("/quality/evolution")
        if evolution and isinstance(evolution, list) and len(evolution) > 0:
            df = pd.DataFrame(evolution)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("date")
                fig = line_chart(df, x="date", y=["controles", "non_conformes"], title="Evolution qualite")
                if fig:
                    st.plotly_chart(fig, width="stretch")

    with tabs[6]:
        st.html(section_header("Controle dimensionnel", "ruler"))
        dims = get_with_filters("/quality/dimensions")
        if dims and isinstance(dims, list) and len(dims) > 0:
            df = pd.DataFrame(dims)
            fig = tolerance_chart(df, title="Controle dimensionnel")
            if fig:
                st.plotly_chart(fig, width="stretch")

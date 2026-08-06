import streamlit as st
import pandas as pd
from dashboard.api_client import get, get_with_filters
from dashboard.charts import (kpi_card, pie_chart, bar_chart, line_chart,
                               donut_chart, status_badge, THEME, progress_bar,
                               section_header)
from dashboard.icons import icon, icon_html


def render():
    st.subheader("Gestion d'Inventaire")

    overview = get_with_filters("/inventory/overview")
    if not overview:
        st.error("Donnees inventaire indisponibles")
        return

    mat = overview.get("matieres", {})
    out = overview.get("outils", {})
    pcs = overview.get("pieces", {})

    st.html(section_header("Vue d'ensemble", "package_icon", "Etat des stocks"))
    st.html(f"""
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:24px">
        {kpi_card("Matieres", mat.get("total", 0), icon_name="package_icon")}
        {kpi_card("Valeur mat.", mat.get("valeur_totale", 0) or 0, unit=" MAD", icon_name="coins")}
        {kpi_card("Outils", out.get("total", 0), icon_name="wrench")}
        {kpi_card("Critiques", out.get("critiques", 0), icon_name="alert_circle")}
        {kpi_card("Pieces", pcs.get("total", 0), icon_name="box")}
        {kpi_card("Valeur stock", (pcs.get("valeur_totale", 0) or 0) + (mat.get("valeur_totale", 0) or 0), unit=" MAD", icon_name="coins")}
    </div>
    """)

    tabs = st.tabs(["Vue d'ensemble", "Alertes", "Matieres premieres", "Outillage", "Pieces"])

    with tabs[0]:
        st.html(section_header("Distribution & Tendances", "chart_bar"))
        col1, col2 = st.columns(2)
        with col1:
            status_dist = get_with_filters("/inventory/status-distribution")
            if status_dist and isinstance(status_dist, dict):
                fig = donut_chart(list(status_dist.keys()), list(status_dist.values()))
                st.plotly_chart(fig, width="stretch")
        with col2:
            value_cat = get_with_filters("/inventory/value-by-category")
            if value_cat and isinstance(value_cat, list) and len(value_cat) > 0:
                df = pd.DataFrame(value_cat)
                fig = bar_chart(df, x="famille", y="valeur_totale")
                if fig:
                    fig.update_traces(marker_color=THEME["primary"], showlegend=False)
                    st.plotly_chart(fig, width="stretch")

        consumption = get_with_filters("/inventory/consumption-trend")
        if consumption and isinstance(consumption, list) and len(consumption) > 0:
            df = pd.DataFrame(consumption)
            fig = line_chart(df, x="mois", y="consommation", fill=True)
            if fig:
                st.plotly_chart(fig, width="stretch")

    with tabs[1]:
        st.html(section_header("Alertes Stock", "alert_triangle", "Articles critiques et bas"))
        alerts = get_with_filters("/inventory/alerts")
        if alerts and isinstance(alerts, list) and len(alerts) > 0:
            for a in alerts:
                statut = a.get("statut", "")
                if statut == "CRITIQUE":
                    color, bg = "#C62828", "#FEF2F2"
                    icon_name = "alert_circle"
                else:
                    color, bg = "#ED6C02", "#FFFBEB"
                    icon_name = "alert_triangle"
                st.html(f"""
                <div style="background:{bg};border:1px solid {color}20;border-left:3px solid {color};
                            border-radius:8px;padding:12px 16px;margin-bottom:5px">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div style="display:flex;align-items:center;gap:8px">
                            <span style="color:{color}">{icon_html(icon_name, 's', color)}</span>
                            <span style="color:#0B2545;font-weight:700;font-family:'Consolas','Courier New',monospace;font-size:12px">{a.get('code','')}</span>
                            <span style="color:#1E293B;font-size:12px">{a.get('designation','')}</span>
                        </div>
                        <div style="display:flex;gap:12px;align-items:center">
                            <span style="color:#64748B;font-size:11px;font-family:'Consolas','Courier New',monospace">Stock: {a.get('quantite_stock',0)} / Seuil: {a.get('seuil_alerte',0)}</span>
                            {status_badge(statut)}
                        </div>
                    </div>
                </div>
                """)
        else:
            st.success("Aucune alerte stock")

    with tabs[2]:
        st.html(section_header("Matieres Premieres", "package_icon"))
        matieres = get_with_filters("/inventory/matieres")
        if matieres and isinstance(matieres, list) and len(matieres) > 0:
            st.dataframe(pd.DataFrame(matieres), width="stretch", hide_index=True)

    with tabs[3]:
        st.html(section_header("Outillage", "wrench"))
        outils = get_with_filters("/inventory/outils")
        if outils and isinstance(outils, list) and len(outils) > 0:
            st.dataframe(pd.DataFrame(outils), width="stretch", hide_index=True)

    with tabs[4]:
        st.html(section_header("Pieces", "box"))
        pieces = get_with_filters("/inventory/pieces")
        if pieces and isinstance(pieces, list) and len(pieces) > 0:
            st.dataframe(pd.DataFrame(pieces), width="stretch", hide_index=True)

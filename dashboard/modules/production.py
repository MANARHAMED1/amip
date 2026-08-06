import streamlit as st
import pandas as pd
from dashboard.api_client import get, get_with_filters
from dashboard.charts import (kpi_card, bar_chart, line_chart, gantt_timeline,
                               progress_bar, status_badge, THEME, section_header)
from dashboard.icons import icon, icon_html


def render():
    st.subheader("Ordres de Fabrication")

    kpi = get_with_filters("/production/kpi")
    if kpi:
        st.html(f"""
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:24px">
            {kpi_card("Total OF", kpi.get("total", 0), icon_name="clipboard_list")}
            {kpi_card("En cours", kpi.get("en_cours", 0), icon_name="refresh")}
            {kpi_card("Termines", kpi.get("termine", 0), icon_name="check_circle")}
            {kpi_card("En attente", kpi.get("en_attente", 0), icon_name="clock")}
            {kpi_card("En retard", kpi.get("en_retard", 0), icon_name="alert_triangle")}
        </div>
        """)

    if "selected_of" in st.session_state:
        _render_detail(st.session_state.selected_of)
        if st.button("Retour a la liste", key="back_btn"):
            del st.session_state.selected_of
            st.rerun()
        return

    st.html(section_header("Filtres", "search"))
    col1, col2 = st.columns([2, 3])
    with col1:
        statut_filter = st.selectbox("Statut", ["Tous", "EN_COURS", "TERMINE", "EN_ATTENTE", "EN_RETARD", "ANNULE"])
    with col2:
        search = st.text_input("Rechercher un OF...", placeholder="Numero, reference, piece...")

    extra = {}
    if statut_filter != "Tous":
        extra["statut"] = statut_filter

    orders = get_with_filters("/production/list", extra_params={**extra, "limit": 200})
    if not orders or not isinstance(orders, list):
        st.warning("Aucune donnee disponible")
        return

    df = pd.DataFrame(orders)
    if search:
        mask = pd.Series([False] * len(df))
        for col_name in ["numero_of", "piece_ref", "piece_nom"]:
            if col_name in df.columns:
                mask = mask | df[col_name].str.contains(search, case=False, na=False)
        df = df[mask]

    if df.empty:
        st.info("Aucun OF correspondant")
        return

    st.html(section_header("Liste des OF", "clipboard_list"))
    for _, row in df.iterrows():
        pct = 0
        if row.get("quantite_demandee", 0) > 0:
            pct = (row.get("quantite_produite", 0) / row["quantite_demandee"]) * 100
        statut = row.get("statut", "")
        sc = THEME["green"] if statut == "EN_COURS" else THEME["primary"] if statut == "TERMINE" else THEME["amber"] if statut in ("EN_ATTENTE", "EN_RETARD") else THEME["text_dim"]

        st.html(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:8px;padding:12px 16px;margin-bottom:5px;
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
                </div>
            </div>
            <div style="margin-top:8px">{progress_bar(pct)}</div>
        </div>
        """)
        if st.button(f"Voir {row['numero_of']}", key=f"view_{row['numero_of']}", width="stretch"):
            st.session_state.selected_of = row["numero_of"]
            st.rerun()


def _render_detail(numero_of):
    detail = get(f"/production/{numero_of}")
    if not detail or "error" in (detail or {}):
        st.error(detail.get("error", "OF introuvable") if detail else "Erreur de chargement")
        return

    of = detail.get("of", {})
    phases = detail.get("phases", [])
    retard = detail.get("retard_jours")

    st.html(section_header(f"OF {numero_of}", "clipboard_list", "Detail de l'ordre de fabrication"))

    st.html(f"""
    <div style="background:white;border:1px solid #E2E8F0;border-radius:12px;padding:18px 22px;margin-bottom:20px;
                box-shadow:0 1px 3px rgba(0,0,0,0.04)">
        <div style="display:flex;align-items:center;gap:14px">
            <span style="color:#0B2545;font-size:22px;font-weight:800;font-family:'Consolas','Courier New',monospace">{numero_of}</span>
            {status_badge(of.get('statut',''))}
            <span style="color:#64748B;font-size:12px">Priorite: {of.get('priorite','')}</span>
            {f'<span style="color:#C62828;font-size:12px;font-weight:700">Retard: {retard}j</span>' if retard and retard > 0 else ''}
        </div>
    </div>
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.html(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;padding:16px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
            <div style="color:#94A3B8;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;font-weight:600">Piece</div>
            <div style="color:#1E293B;font-size:13px;font-weight:600">{of.get('piece_ref','')} - {of.get('piece_nom','')}</div>
            <div style="color:#64748B;font-size:11px;margin-top:3px">{of.get('famille','')} - {of.get('matiere_nom','')}</div>
        </div>
        """)
    with col2:
        q_prod = of.get("quantite_produite", 0) or 0
        q_dem = of.get("quantite_demandee", 0) or 1
        st.html(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;padding:16px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
            <div style="color:#94A3B8;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;font-weight:600">Quantites</div>
            <div style="color:#1E293B;font-size:12px">Demandees: <b>{of.get('quantite_demandee',0)}</b></div>
            <div style="color:#1E293B;font-size:12px">Produites: <b>{q_prod}</b></div>
            <div style="color:#C62828;font-size:12px">Rebut: <b>{of.get('quantite_rebut',0)}</b></div>
        </div>
        """)
    with col3:
        rendement = (q_prod / q_dem * 100) if q_dem > 0 else 0
        st.html(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;padding:16px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
            <div style="color:#94A3B8;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;font-weight:600">Rendement</div>
            <div style="color:#1E293B;font-size:28px;font-weight:800;font-family:'Consolas','Courier New',monospace">{rendement:.1f}%</div>
            <div style="margin-top:8px">{progress_bar(rendement)}</div>
        </div>
        """)

    if phases:
        st.html(section_header("Phases", "layers"))
        df_phases = pd.DataFrame(phases)
        cols_show = ["numero_phase", "designation", "machine_code", "outil_code",
                     "temps_usinage_prevu", "temps_usinage_reel", "nb_pieces_produites", "nb_pieces_rebut", "statut"]
        cols_exist = [c for c in cols_show if c in df_phases.columns]
        st.dataframe(df_phases[cols_exist], width="stretch", hide_index=True)

        gantt_data = df_phases.copy()
        if "date_debut" in gantt_data.columns and "date_fin" in gantt_data.columns:
            for col in ["date_debut", "date_fin"]:
                gantt_data[col] = pd.to_datetime(gantt_data[col], errors="coerce")
            gantt_data = gantt_data.dropna(subset=["date_debut", "date_fin"])
            if not gantt_data.empty:
                fig = gantt_timeline(gantt_data, title="Timeline phases")
                if fig:
                    st.plotly_chart(fig, width="stretch")

    eff = get(f"/production/{numero_of}/efficiency")
    if eff:
        st.html(f"""
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px">
            {kpi_card("Efficacite globale", round(eff.get("efficacite_globale", 0) * 100, 1), unit="%", icon_name="chart_bar")}
            {kpi_card("Efficacite temps", round(eff.get("efficacite_temps", 0) * 100, 1), unit="%", icon_name="timer")}
            {kpi_card("Nb phases", len(eff.get("phases", [])), icon_name="clipboard_list")}
        </div>
        """)

import streamlit as st
import pandas as pd
import time
from dashboard.api_client import get, get_with_filters
from dashboard.charts import (kpi_metric, line_chart, bar_chart, heatmap_chart,
                               scatter_chart, machine_card_html, THEME, section_header)
from dashboard.icons import icon, icon_html


def render():
    st.subheader("Capteurs & Temps Reel")
    st.caption("Surveillance en temps reel des capteurs CNC")

    all_machines = get("/sensors/all-machines")
    if not all_machines or not isinstance(all_machines, list):
        st.error("Donnees capteurs indisponibles - verifiez que le backend est actif")
        return

    _render_machine_grid(all_machines)

    st.html('<div style="margin:16px 0;border-top:1px solid var(--border)"></div>')

    codes = [m.get("code", "") for m in all_machines if m.get("code")]
    if not codes:
        st.warning("Aucune machine disponible")
        return

    col_sel, col_refresh = st.columns([5, 1])
    with col_sel:
        selected = st.selectbox("Selectionner une machine", codes, label_visibility="visible",
                                key="sensor_machine_select")
    with col_refresh:
        auto_refresh = st.toggle("Auto-refresh", value=False, key="sensor_auto_refresh")

    if auto_refresh:
        time.sleep(5)
        st.rerun()

    tabs = st.tabs(["Evolution", "Statistiques", "Heatmap", "Correlation", "Alertes"])

    with tabs[0]:
        _render_evolution(selected)
    with tabs[1]:
        _render_stats(selected)
    with tabs[2]:
        _render_heatmap(selected)
    with tabs[3]:
        _render_correlation(selected)
    with tabs[4]:
        _render_alerts(selected)


def _render_machine_grid(all_machines):
    n = len(all_machines)
    cols_per_row = min(6, max(3, n))
    rows = [all_machines[i:i + cols_per_row] for i in range(0, n, cols_per_row)]

    for row_machines in rows:
        cols = st.columns(len(row_machines))
        for col, m in zip(cols, row_machines):
            with col:
                code = m.get("code", "?")
                statut = m.get("statut_machine", "UNKNOWN")
                t = m.get("temperature", 0) or 0
                v = m.get("vibration", 0) or 0
                rpm = m.get("rpm", 0) or 0

                if statut == "RUNNING":
                    dot_color = THEME["green"]
                    dot_pulse = "animation:statusPulse 2s infinite"
                elif statut in ("STOPPED", "BROKEN"):
                    dot_color = THEME["red"]
                    dot_pulse = ""
                else:
                    dot_color = THEME["amber"]
                    dot_pulse = ""

                temp_color = THEME["red"] if t > 60 else THEME["amber"] if t > 45 else THEME["text"]
                vib_color = THEME["red"] if v > 2.5 else THEME["amber"] if v > 1.5 else THEME["text"]

                st.html(f"""
                <div style="background:{THEME['card']};border:1px solid {THEME['border']};border-radius:10px;
                            padding:14px 16px;transition:all 0.25s cubic-bezier(0.4,0,0.2,1);height:100%">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                        <span style="color:{THEME['accent_light']};font-weight:700;font-size:13px;font-family:'Consolas','Courier New',monospace">{code}</span>
                        <span style="width:7px;height:7px;background:{dot_color};border-radius:50%;display:inline-block;{dot_pulse}"></span>
                    </div>
                    <div style="display:flex;flex-direction:column;gap:4px">
                        <div style="display:flex;justify-content:space-between;font-size:11px">
                            <span style="color:{THEME['text_dim']}">Temp</span>
                            <span style="color:{temp_color};font-family:'Consolas','Courier New',monospace;font-weight:600">{t:.1f}&deg;C</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:11px">
                            <span style="color:{THEME['text_dim']}">Vib</span>
                            <span style="color:{vib_color};font-family:'Consolas','Courier New',monospace;font-weight:600">{v:.2f}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:11px">
                            <span style="color:{THEME['text_dim']}">RPM</span>
                            <span style="color:{THEME['text']};font-family:'Consolas','Courier New',monospace;font-weight:600">{rpm:.0f}</span>
                        </div>
                    </div>
                </div>
                """)


def _render_evolution(selected):
    history = get_with_filters(f"/sensors/history/{selected}")
    if not history or not isinstance(history, list) or len(history) == 0:
        st.info("Aucune donnee historique pour cette machine")
        return

    df = pd.DataFrame(history)
    if "timestamp" not in df.columns:
        st.info("Format de donnees inattendu")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    sensor_cols = [c for c in ["temperature", "vibration", "rpm", "puissance"] if c in df.columns]

    if not sensor_cols:
        st.info("Aucune donnee capteur disponible")
        return

    fig = line_chart(df, x="timestamp", y=sensor_cols, title="Evolution des capteurs")
    if fig:
        fig.update_layout(legend=dict(orientation="h", y=-0.18))
        st.plotly_chart(fig, width="stretch")

    if len(sensor_cols) >= 2:
        st.html(section_header("Capteurs Individuels", "activity"))
        sub_cols = st.columns(min(len(sensor_cols), 2))
        for i, col_name in enumerate(sensor_cols):
            with sub_cols[i % len(sub_cols)]:
                fig2 = line_chart(df, x="timestamp", y=col_name, title=col_name.replace("_", " ").title())
                if fig2:
                    st.plotly_chart(fig2, width="stretch")


def _render_stats(selected):
    stats = get(f"/sensors/stats/{selected}")
    if not stats or not isinstance(stats, dict):
        st.info("Statistiques non disponibles")
        return

    alertes_total = (stats.get("alertes_temp", 0) or 0) + (stats.get("alertes_vibration", 0) or 0)

    st.html(section_header("Statistiques", "bar_chart"))
    st.html(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px">
        {kpi_metric("Temperature moy.", stats.get('temp_moy', 0) or 0, unit="&deg;C")}
        {kpi_metric("Vibration moy.", stats.get('vib_moy', 0) or 0, unit=" mm/s")}
        {kpi_metric("RPM moyen", stats.get('rpm_moy', 0) or 0)}
        {kpi_metric("Alertes totales", alertes_total)}
    </div>
    """)

    st.html(section_header("Plages de valeurs", "sliders"))
    detail_cols = st.columns(3)
    with detail_cols[0]:
        st.html(f"""
        <div style="background:{THEME['card']};border:1px solid {THEME['border']};border-radius:10px;padding:16px">
            <div style="color:{THEME['text_dim']};font-size:10.5px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;font-weight:600">Temperature</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="color:{THEME['text_dim']};font-size:12px">Min</span>
                <span style="color:{THEME['text']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('temp_min',0):.1f}&deg;C</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="color:{THEME['text_dim']};font-size:12px">Moy</span>
                <span style="color:{THEME['accent_light']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('temp_moy',0):.1f}&deg;C</span>
            </div>
            <div style="display:flex;justify-content:space-between">
                <span style="color:{THEME['text_dim']};font-size:12px">Max</span>
                <span style="color:{THEME['red']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('temp_max',0):.1f}&deg;C</span>
            </div>
        </div>
        """)
    with detail_cols[1]:
        st.html(f"""
        <div style="background:{THEME['card']};border:1px solid {THEME['border']};border-radius:10px;padding:16px">
            <div style="color:{THEME['text_dim']};font-size:10.5px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;font-weight:600">Vibration</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="color:{THEME['text_dim']};font-size:12px">Min</span>
                <span style="color:{THEME['text']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('vib_min',0):.2f} mm/s</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="color:{THEME['text_dim']};font-size:12px">Moy</span>
                <span style="color:{THEME['accent_light']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('vib_moy',0):.2f} mm/s</span>
            </div>
            <div style="display:flex;justify-content:space-between">
                <span style="color:{THEME['text_dim']};font-size:12px">Max</span>
                <span style="color:{THEME['red']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('vib_max',0):.2f} mm/s</span>
            </div>
        </div>
        """)
    with detail_cols[2]:
        st.html(f"""
        <div style="background:{THEME['card']};border:1px solid {THEME['border']};border-radius:10px;padding:16px">
            <div style="color:{THEME['text_dim']};font-size:10.5px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;font-weight:600">Puissance</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="color:{THEME['text_dim']};font-size:12px">Moy</span>
                <span style="color:{THEME['accent_light']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('puissance_moy',0):.1f} kW</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="color:{THEME['text_dim']};font-size:12px">Max</span>
                <span style="color:{THEME['amber']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('puissance_max',0):.1f} kW</span>
            </div>
            <div style="display:flex;justify-content:space-between">
                <span style="color:{THEME['text_dim']};font-size:12px">Lectures</span>
                <span style="color:{THEME['text']};font-size:13px;font-family:'Consolas','Courier New',monospace;font-weight:600">{stats.get('nb_readings',0)}</span>
            </div>
        </div>
        """)


def _render_heatmap(selected):
    st.html(section_header("Heatmap", "grid"))
    heatmap_data = get(f"/sensors/heatmap/{selected}")
    if not heatmap_data or not isinstance(heatmap_data, list) or len(heatmap_data) == 0:
        st.info("Pas de donnees heatmap disponibles")
        return

    df = pd.DataFrame(heatmap_data)
    metrics = [m for m in ["temperature", "vibration", "puissance"] if m in df.columns]
    has_grid = "jour" in df.columns and "heure" in df.columns

    if not has_grid:
        st.info("Format heatmap inattendu")
        return

    day_labels = {0: "Dim", 1: "Lun", 2: "Mar", 3: "Mer", 4: "Jeu", 5: "Ven", 6: "Sam"}

    for metric in metrics:
        pivot = df.pivot_table(index="jour", columns="heure", values=metric, aggfunc="mean")
        pivot.index = pivot.index.map(lambda x: day_labels.get(int(x), str(int(x))))
        fig = heatmap_chart(pivot, title=f"Heatmap {metric.replace('_', ' ').title()}")
        if fig:
            st.plotly_chart(fig, width="stretch")


def _render_correlation(selected):
    st.html(section_header("Correlation", "scatter"))
    corr_data = get(f"/sensors/correlation/{selected}")
    if not corr_data or not isinstance(corr_data, list) or len(corr_data) == 0:
        st.info("Pas de donnees de correlation disponibles")
        return

    df = pd.DataFrame(corr_data)
    num_cols = [c for c in ["temperature", "vibration", "rpm", "puissance", "charge_frappe"] if c in df.columns]

    if len(num_cols) < 2:
        st.info("Pas assez de variables numeriques pour une correlation")
        return

    col_a, col_b = st.columns(2)
    with col_a:
        x_col = st.selectbox("Axe X", num_cols, index=0, key="corr_x",
                             format_func=lambda c: c.replace("_", " ").title())
    with col_b:
        y_col = st.selectbox("Axe Y", num_cols, index=min(1, len(num_cols) - 1), key="corr_y",
                             format_func=lambda c: c.replace("_", " ").title())

    fig = scatter_chart(df, x=x_col, y=y_col,
                        title=f"{x_col.replace('_',' ').title()} vs {y_col.replace('_',' ').title()}",
                        trendline=True)
    if fig:
        st.plotly_chart(fig, width="stretch")


def _render_alerts(selected):
    st.html(section_header("Alertes Capteurs", "alert_triangle"))
    alerts = get(f"/sensors/alerts/{selected}")
    if not alerts or not isinstance(alerts, list) or len(alerts) == 0:
        st.success("Aucune alerte capteur pour cette machine")
        return

    df = pd.DataFrame(alerts)
    n_critique = len(df[df.get("niveau", pd.Series()) == "CRITIQUE"]) if "niveau" in df.columns else 0
    n_attention = len(df[df.get("niveau", pd.Series()) == "ATTENTION"]) if "niveau" in df.columns else 0

    st.html(f"""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px">
        {kpi_metric("Total alertes", len(df))}
        {kpi_metric("Critiques", n_critique)}
        {kpi_metric("Attention", n_attention)}
    </div>
    """)

    for _, row in df.iterrows():
        niveau = row.get("niveau", "")
        if niveau == "CRITIQUE":
            color = THEME["red"]
            bg = "rgba(239,83,80,0.06)"
            border = "rgba(239,83,80,0.25)"
        elif niveau == "ATTENTION":
            color = THEME["amber"]
            bg = "rgba(224,160,38,0.06)"
            border = "rgba(224,160,38,0.25)"
        else:
            color = THEME["accent"]
            bg = "rgba(56,152,236,0.06)"
            border = "rgba(56,152,236,0.25)"

        st.html(f"""
        <div style="background:{bg};border:1px solid {border};border-left:3px solid {color};
                    border-radius:8px;padding:12px 16px;margin-bottom:6px">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div style="display:flex;align-items:center;gap:12px">
                    <span style="color:{THEME['text_dim']};font-size:12px;font-family:'Consolas','Courier New',monospace">{str(row.get('timestamp',''))[:19]}</span>
                    <span style="color:{THEME['text']};font-size:12px">
                        T: <b style="font-family:'Consolas','Courier New',monospace">{row.get('temperature',0):.1f}</b>&deg;C
                        &nbsp;&middot;&nbsp;
                        V: <b style="font-family:'Consolas','Courier New',monospace">{row.get('vibration',0):.2f}</b> mm/s
                    </span>
                </div>
                <span style="color:{color};font-size:11px;font-weight:600;letter-spacing:0.04em">{niveau}</span>
            </div>
        </div>
        """)

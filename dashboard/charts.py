import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dashboard.icons import icon, icon_html

PRIMARY = "#0B2545"
ACCENT = "#5B7B9A"
SUCCESS = "#2E7D32"
WARNING = "#ED6C02"
DANGER = "#C62828"
TEXT = "#1C1E21"
TEXT_DIM = "#5A6872"
TEXT_LIGHT = "#8A95A0"
BG = "#F4F6F8"
CARD = "#FFFFFF"
BORDER = "#E2E5E9"

THEME = {
    "bg": BG, "card": CARD, "border": BORDER, "text": TEXT, "text_dim": TEXT_LIGHT,
    "primary": PRIMARY, "accent": ACCENT, "green": SUCCESS, "amber": WARNING,
    "red": DANGER,
}

CHART_COLORS = ["#0B2545", "#1A3A5C", "#2E5274", "#5B7B9A", "#7B95B0", "#9DB3C8", "#C4D3E2", "#E4EBF2"]

LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, family="system-ui, -apple-system, sans-serif", size=12),
    margin=dict(l=10, r=10, t=44, b=10),
    xaxis=dict(gridcolor="#E4E8ED", zerolinecolor="#E2E5E9", linecolor="#E2E5E9",
               tickfont=dict(family="'Consolas', 'Courier New', monospace", size=10, color=TEXT_DIM)),
    yaxis=dict(gridcolor="#E4E8ED", zerolinecolor="#E2E5E9", linecolor="#E2E5E9",
               tickfont=dict(family="'Consolas', 'Courier New', monospace", size=10, color=TEXT_DIM)),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
                font=dict(family="system-ui, -apple-system, sans-serif", size=11, color=TEXT_DIM)),
    hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER,
                    font=dict(family="system-ui, -apple-system, sans-serif", size=12, color=TEXT)),
    title=dict(font=dict(family="system-ui, -apple-system, sans-serif", size=14, color=TEXT), x=0, xanchor="left"),
)


def section_header(title: str, icon_name: str = "", subtitle: str = ""):
    icon_str = f'<span style="color:{PRIMARY}">{icon(icon_name, "s")}</span>' if icon_name else ""
    sub = f'<div style="color:{TEXT_LIGHT};font-size:12px;margin-top:2px">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="display:flex;align-items:center;gap:8px;margin:28px 0 14px 4px">
        {icon_str}
        <div>
            <div style="color:{TEXT};font-size:15px;font-weight:700;letter-spacing:-0.01em">{title}</div>
            {sub}
        </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,{BORDER} 0%,rgba(226,229,233,0.3) 100%);margin:0 0 16px 0"></div>
    """


def kpi_card(label: str, value, delta=None, unit="", icon_name="", subtitle=""):
    val_str = f"{value:,.1f}" if isinstance(value, (int, float)) else str(value)
    if unit:
        val_str += unit

    delta_html = ""
    if delta is not None:
        d_color = SUCCESS if delta >= 0 else DANGER
        arrow_svg = icon("arrow_up", "s") if delta >= 0 else icon("arrow_down", "s")
        delta_html = f'<span style="color:{d_color};font-size:11px;margin-left:6px;font-family:Consolas,monospace;display:inline-flex;align-items:center;gap:2px">{arrow_svg} {abs(delta):.1f}%</span>'

    icon_html_str = ""
    if icon_name:
        svg = icon(icon_name, "s")
        icon_html_str = f'<span style="color:{PRIMARY};display:inline-flex;margin-bottom:8px">{svg}</span>'

    return f"""
    <div class="card-lift" style="background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:16px 18px;
                box-shadow:0 1px 2px rgba(0,0,0,0.04);transition:all 0.2s cubic-bezier(0.4,0,0.2,1);
                border-top:3px solid;border-image:linear-gradient(90deg,{PRIMARY},{ACCENT}) 1;
                border-image-slice:1;border-top-style:solid">
        {icon_html_str}
        <div style="color:{TEXT_DIM};font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;font-weight:600">{label}</div>
        <div style="color:{TEXT};font-size:24px;font-weight:700;font-family:'Consolas','Courier New',monospace;line-height:1.2">{val_str}{delta_html}</div>
        {"<div style='color:"+TEXT_LIGHT+";font-size:11px;margin-top:3px'>"+subtitle+"</div>" if subtitle else ""}
    </div>
    """


def kpi_metric(label: str, value, unit=""):
    val_str = f"{value:,.1f}" if isinstance(value, (int, float)) else str(value)
    if unit:
        val_str += unit
    return f"""
    <div class="card-lift" style="background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:14px 16px;
                box-shadow:0 1px 2px rgba(0,0,0,0.04);transition:all 0.2s cubic-bezier(0.4,0,0.2,1);
                border-top:2px solid;border-image:linear-gradient(90deg,{PRIMARY},{ACCENT}) 1;
                border-image-slice:1;border-top-style:solid">
        <div style="color:{TEXT_LIGHT};font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px;font-weight:600">{label}</div>
        <div style="color:{TEXT};font-size:22px;font-weight:700;font-family:'Consolas','Courier New',monospace;line-height:1.2">{val_str}</div>
    </div>
    """


def status_badge(status: str):
    styles = {
        "RUNNING": (SUCCESS, "En marche"),
        "STOPPED": (TEXT_DIM, "Arretee"),
        "MAINTENANCE": (WARNING, "Maintenance"),
        "BROKEN": (DANGER, "En panne"),
        "EN_COURS": (SUCCESS, "En cours"),
        "TERMINE": (PRIMARY, "Termine"),
        "EN_ATTENTE": (WARNING, "En attente"),
        "ANNULE": (TEXT_DIM, "Annule"),
        "EN_RETARD": (DANGER, "En retard"),
        "CRITIQUE": (DANGER, "Critique"),
        "BAS": (WARNING, "Bas"),
        "NORMAL": (SUCCESS, "Normal"),
        "SURSTOCK": (ACCENT, "Surstock"),
    }
    color, label = styles.get(status, (TEXT_DIM, status))
    return (
        f'<span style="background:{color}10;color:{color};padding:3px 10px;border-radius:12px;'
        f'font-size:11px;font-weight:600;border:1px solid {color}18;'
        f'display:inline-flex;align-items:center;gap:4px;transition:all 0.15s ease">'
        f'<span style="width:6px;height:6px;background:{color};border-radius:50%;display:inline-block"></span>'
        f'{label}</span>'
    )


def gauge_chart(value: float, title: str, max_val: float = 100, thresholds: dict = None):
    if thresholds is None:
        thresholds = {"green": 70, "orange": 40}
    g_t = thresholds.get("green", 70)
    o_t = thresholds.get("orange", 40)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        number=dict(suffix="%", font=dict(size=32, color=TEXT, family="Consolas, monospace")),
        title=dict(text=title, font=dict(size=12, color=TEXT_DIM, family="system-ui, sans-serif")),
        gauge=dict(
            axis=dict(range=[0, max_val], tickcolor=TEXT_LIGHT),
            bar=dict(color=PRIMARY, thickness=0.5),
            bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", borderwidth=0,
            steps=[
                dict(range=[0, o_t], color="#FFE0D6"),
                dict(range=[o_t, g_t], color="#FFF1CC"),
                dict(range=[g_t, max_val], color="#D8EDDA"),
            ],
            threshold=dict(line=dict(color=TEXT, width=3), thickness=0.75, value=value),
        ),
    ))
    fig.update_layout(**{**LAYOUT, "height": 220, "margin": dict(l=24, r=24, t=36, b=8)})
    return fig


def bar_chart(df, x, y, color=None, title="", horizontal=False, color_discrete_map=None):
    if df is None or df.empty:
        return None
    fig = px.bar(df, x=y if horizontal else x, y=x if horizontal else y,
                 color=color, title=title, color_discrete_map=color_discrete_map,
                 orientation="h" if horizontal else "v",
                 color_discrete_sequence=CHART_COLORS)
    fig.update_layout(**LAYOUT, height=340)
    fig.update_traces(marker_line_width=0, marker=dict(opacity=0.85, cornerradius=4),
                      hoverlabel=dict(bgcolor=CARD))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F0F2F5")
    return fig


def line_chart(df, x, y, title="", fill=False, smooth=True):
    if df is None or df.empty:
        return None
    fig = px.area if fill else px.line
    fig = fig(df, x=x, y=y, title=title, color_discrete_sequence=CHART_COLORS)
    for tr in fig.data:
        ln = dict(width=2.5)
        if smooth and tr.type == "scatter":
            ln["shape"] = "spline"
        tr.update(line=ln, hoverlabel=dict(bgcolor=CARD))
    if fill:
        for i in range(len(fig.data)):
            c = CHART_COLORS[i % len(CHART_COLORS)]
            fig.data[i].update(fill="tozeroy", fillcolor=f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.08)")
    fig.update_layout(**LAYOUT, height=300)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F0F2F5")
    return fig


def multi_line_chart(df, x, y_list, title=""):
    if df is None or df.empty:
        return None
    fig = px.line(df, x=x, y=y_list, title=title, color_discrete_sequence=CHART_COLORS)
    for tr in fig.data:
        ln = dict(width=2.5)
        if tr.type == "scatter":
            ln["shape"] = "spline"
        tr.update(line=ln, hoverlabel=dict(bgcolor=CARD))
    fig.update_layout(**LAYOUT, height=300)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F0F2F5")
    return fig


def pie_chart(df, names, values, title=""):
    if df is None or df.empty:
        return None
    fig = px.pie(df, names=names, values=values, title=title, color_discrete_sequence=CHART_COLORS)
    fig.update_layout(**LAYOUT, height=300)
    fig.update_traces(textfont_size=12, marker=dict(line=dict(color=CARD, width=3)),
                      hoverlabel=dict(bgcolor=CARD), hole=0.4,
                      pull=[0.02] + [0] * (len(df) - 1))
    return fig


def scatter_chart(df, x, y, title="", color=None, trendline=False):
    if df is None or df.empty:
        return None
    use_trendline = None
    if trendline:
        try:
            import statsmodels.api
            use_trendline = "ols"
        except ImportError:
            pass
    fig = px.scatter(df, x=x, y=y, color=color, title=title,
                     trendline=use_trendline, color_discrete_sequence=CHART_COLORS)
    fig.update_layout(**LAYOUT, height=340)
    fig.update_traces(hoverlabel=dict(bgcolor=CARD), marker=dict(size=8, opacity=0.8, line=dict(width=1, color=CARD)))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F0F2F5")
    return fig


def heatmap_chart(df_pivot, title=""):
    if df_pivot is None or df_pivot.empty:
        return None
    fig = px.imshow(df_pivot, title=title,
                    color_continuous_scale=["#E4E8ED", "#C4D3E2", "#7B95B0", PRIMARY])
    fig.update_layout(**LAYOUT, height=340)
    return fig


def gantt_timeline(df, title=""):
    if df is None or df.empty:
        return None
    df = df.copy()
    if "date_debut" not in df.columns or "date_fin" not in df.columns:
        return None
    for col in ["date_debut", "date_fin"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df = df.dropna(subset=["date_debut", "date_fin"])
    if df.empty:
        return None
    fig = px.timeline(df, x_start="date_debut", x_end="date_fin",
                      y="phase_name" if "phase_name" in df.columns else df.columns[0],
                      color="statut" if "statut" in df.columns else None,
                      color_discrete_map={"TERMINE": SUCCESS, "EN_COURS": WARNING, "EN_ATTENTE": TEXT_LIGHT})
    fig.update_layout(**LAYOUT, height=min(380, max(260, len(df) * 34)))
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
    fig.update_traces(hoverlabel=dict(bgcolor=CARD), marker=dict(cornerradius=4))
    return fig


def tolerance_chart(df, title=""):
    if df is None or df.empty:
        return None
    fig = go.Figure()
    if "dimension_mesuree" in df.columns and "dimension_cible" in df.columns:
        target = df["dimension_cible"].iloc[0] if not df["dimension_cible"].isna().all() else 0
        tol_plus = df["tolerance_plus"].iloc[0] if "tolerance_plus" in df.columns and not df["tolerance_plus"].isna().all() else 0
        tol_minus = df["tolerance_moins"].iloc[0] if "tolerance_moins" in df.columns and not df["tolerance_moins"].isna().all() else 0
        x = range(len(df))
        fig.add_trace(go.Scatter(x=list(x), y=df["dimension_mesuree"], mode="markers",
                                 marker=dict(color=PRIMARY, size=8, line=dict(width=1, color=CARD)), name="Mesure"))
        fig.add_hline(y=target, line=dict(color=SUCCESS, width=2, dash="dash"), annotation_text="Cible")
        if tol_plus:
            fig.add_hline(y=target + tol_plus, line=dict(color=WARNING, width=1, dash="dot"))
        if tol_minus:
            fig.add_hline(y=target - abs(tol_minus), line=dict(color=WARNING, width=1, dash="dot"))
    fig.update_layout(**LAYOUT, height=300)
    return fig


def progress_bar(value: float, max_val: float = 100, color: str = None):
    if color is None:
        if value >= 80:
            color = SUCCESS
        elif value >= 50:
            color = WARNING
        else:
            color = DANGER
    pct = min(100, max(0, value / max_val * 100)) if max_val > 0 else 0
    return f"""
    <div style="background:#E4E8ED;border-radius:4px;height:6px;width:100%;overflow:hidden">
        <div style="background:linear-gradient(90deg,{color}cc,{color});border-radius:4px;height:6px;width:{pct}%;
                    transition:width 0.6s cubic-bezier(0.4,0,0.2,1)"></div>
    </div>
    """


def donut_chart(labels, values, title=""):
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.65,
                           marker=dict(colors=CHART_COLORS, line=dict(color=CARD, width=3)),
                           textfont=dict(size=12, family="system-ui, sans-serif"),
                           hoverlabel=dict(bgcolor=CARD),
                           pull=[0.02] + [0] * (len(labels) - 1)))
    fig.update_layout(**{**LAYOUT, "height": 260, "title": dict(text=title, font=dict(size=13)),
                         "showlegend": True, "legend": dict(font=dict(size=10))})
    return fig


def machine_card_html(m: dict):
    s = m.get("statut", "UNKNOWN")
    if s == "RUNNING":
        color = SUCCESS
    elif s in ("STOPPED", "BROKEN"):
        color = DANGER
    else:
        color = WARNING

    badge = status_badge(s)

    return f"""
    <div class="card-lift" style="background:{CARD};border:1px solid {BORDER};border-radius:8px;padding:12px 14px;
                margin-bottom:5px;box-shadow:0 1px 2px rgba(0,0,0,0.03);transition:all 0.2s cubic-bezier(0.4,0,0.2,1);
                border-left:3px solid {color}">
        <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
                <span style="color:{TEXT};font-weight:700;font-size:13px;font-family:'Consolas','Courier New',monospace">{m.get('code','')}</span>
                <span style="color:{TEXT_DIM};font-size:12px;margin-left:8px">{m.get('nom','')}</span>
            </div>
            {badge}
        </div>
        <div style="color:{TEXT_LIGHT};font-size:11px;margin-top:4px">{m.get('type','')} - {m.get('marque','')} {m.get('modele','')}</div>
    </div>
    """

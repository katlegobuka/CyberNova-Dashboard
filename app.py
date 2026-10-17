"""
CyberNova Analytics Ltd - Sales Analytics Dashboard v2
Sophisticated Emerald Theme | Plotly Interactive Charts
BSc Business Intelligence & Data Analytics - CET333
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
import os, warnings
warnings.filterwarnings("ignore")

# PAGE CONFIG

st.set_page_config(
    page_title="CyberNova - Sales Analytics",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# COLOUR PALETTE  - Sophisticated Emerald 2026

C = {
    "primary":    "#156450",   # Emerald Green
    "primary_lt": "#1a8068",   # Lighter emerald
    "primary_dk": "#0d4035",   # Dark emerald
    "bg":         "#FDFCFB",   # Off-White/Sand
    "bg2":        "#E9EDF0",   # Light Slate
    "text":       "#0A2E26",   # Deep Forest
    "text_muted": "#4A7568",
    "success":    "#16A34A",
    "warning":    "#D97706",
    "danger":     "#DC2626",
    "border":     "#C8D5D1",
    "white":      "#FFFFFF",
    "cat": [                   # Categorical 7-colour palette
        "#156450","#2D9B7A","#5BB89A","#A8D5C7",
        "#D97706","#2563EB","#7C3AED",
    ],
}


# GLOBAL CSS

st.markdown(f"""
<style>
  /* ── Reset & base ─────────────────────────────────── */
  html, body, [data-testid="stAppViewContainer"] {{
    background: {C['bg']} !important;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    color: {C['text']};
  }}
  [data-testid="stMain"] {{ background: {C['bg']} !important; }}
  .main .block-container {{ padding: 1.5rem 2rem 3rem; max-width: 1400px; }}

  /* ── Sidebar ───────────────────────────────────────── */
  [data-testid="stSidebar"] {{
    background: {C['primary_dk']} !important;
    border-right: 1px solid {C['primary']};
  }}
  [data-testid="stSidebar"] * {{
    color: #d4ede7 !important;
  }}
  [data-testid="stSidebar"] .stSelectbox > div > div,
  [data-testid="stSidebar"] .stMultiSelect > div > div {{
    background: {C['primary']} !important;
    border: 1px solid {C['primary_lt']} !important;
    color: white !important;
  }}
  [data-testid="stSidebar"] .stDateInput input {{
    background: {C['primary']} !important;
    color: white !important;
    border: 1px solid {C['primary_lt']} !important;
  }}
  [data-testid="stSidebar"] hr {{ border-color: {C['primary']} !important; opacity:0.4; }}

  /* ── Metric cards ──────────────────────────────────── */
  [data-testid="stMetric"] {{
    background: {C['white']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    /* border removed per user request - uniform border colour */
  }}
  [data-testid="stMetricValue"] {{
    color: {C['primary']} !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
  }}
  [data-testid="stMetricLabel"] {{
    color: {C['text_muted']} !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
  }}
  [data-testid="stMetricDelta"] {{ font-size: 0.8rem !important; background: transparent !important; }}

  /* ── Responsive metric grid ────────────────────────── */
  .metric-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }}
  .metric-grid-item {{
    background: {C['white']};
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 1rem 1.25rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .metric-grid-label {{
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: {C['text_muted']};
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .metric-grid-value {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {C['primary']};
    line-height: 1.2;
    word-break: break-word;
  }}
  .metric-grid-delta {{
    font-size: 0.8rem;
    color: {C['text_muted']};
    margin-top: 2px;
  }}

  /* ── Tabs ──────────────────────────────────────────── */
  .stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: {C['bg2']} !important;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid {C['border']};
  }}
  .stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    border-radius: 7px !important;
    color: {C['text_muted']} !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    border: none !important;
  }}
  .stTabs [aria-selected="true"] {{
    background: {C['primary']} !important;
    color: {C['white']} !important;
    font-weight: 600 !important;
  }}

  /* ── Cards ─────────────────────────────────────────── */
  .em-card {{
    background: {C['white']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
  }}
  .em-card-title {{
    font-size: 0.8rem;
    font-weight: 700;
    color: {C['text_muted']};
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin: 0 0 0.75rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  /* ── Page header ───────────────────────────────────── */
  .page-header {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 1.5rem;
    padding-bottom: 1.25rem;
    border-bottom: 2px solid {C['border']};
  }}
  .page-header-logo {{
    width: 44px; height: 44px;
    background: {C['primary']};
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }}
  .page-header-title {{ font-size: 1.5rem; font-weight: 700; color: {C['text']}; margin: 0; }}
  .page-header-sub {{ font-size: 0.8rem; color: {C['text_muted']}; margin: 2px 0 0; }}

  /* ── Section label ─────────────────────────────────── */
  .section-label {{
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {C['text_muted']};
    margin: 1.5rem 0 0.75rem;
    display: flex; align-items: center; gap: 8px;
  }}
  .section-label::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: {C['border']};
  }}

  /* ── Funnel bars ───────────────────────────────────── */
  .funnel-wrap {{ margin-top: 8px; }}
  .funnel-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 9px; }}
  .funnel-label {{ font-size: 12px; color: {C['text_muted']}; width: 130px; flex-shrink: 0; text-align: right; }}
  .funnel-track {{ flex: 1; height: 24px; background: {C['bg2']}; border-radius: 6px; overflow: hidden; }}
  .funnel-fill {{
    height: 100%; display: flex; align-items: center;
    padding: 0 10px; font-size: 11px; font-weight: 600;
    border-radius: 6px; color: white; white-space: nowrap;
    transition: width 0.5s ease;
  }}
  .funnel-pct {{ font-size: 12px; color: {C['text_muted']}; width: 38px; text-align: right; flex-shrink: 0; }}

  /* ── KPI summary row ───────────────────────────────── */
  .kpi-band {{
    background: {C['primary']};
    border-radius: 12px;
    padding: 1rem 1.5rem;
    display: flex;
    gap: 0;
    margin-bottom: 1.5rem;
    color: white;
  }}
  .kpi-band-item {{
    flex: 1;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.2);
    padding: 0 1rem;
  }}
  .kpi-band-item:last-child {{ border-right: none; }}
  .kpi-band-label {{ font-size: 0.68rem; opacity: 0.75; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px; }}
  .kpi-band-value {{ font-size: 1.4rem; font-weight: 700; }}

  /* ── Table style ───────────────────────────────────── */
  .stDataFrame {{ border-radius: 10px; overflow: hidden; }}

  /* ── Sidebar brand ─────────────────────────────────── */
  .sb-brand {{
    display: flex; align-items: center; gap: 10px;
    padding: 0.5rem 0 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 1rem;
  }}
  .sb-logo {{
    width: 36px; height: 36px;
    background: {C['primary_lt']};
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }}
  .sb-title {{ font-size: 13px; font-weight: 700; color: white !important; margin: 0; }}
  .sb-sub {{ font-size: 10px; opacity: 0.65; color: white !important; margin: 1px 0 0; }}

  /* ── Insight badge ─────────────────────────────────── */
  .insight-row {{
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 12px; background: {C['bg2']};
    border-radius: 8px; margin-bottom: 7px;
    font-size: 13px; color: {C['text']};
  }}
  .insight-icon {{ flex-shrink: 0; margin-top: 1px; }}

  /* ── No-data message ───────────────────────────────── */
  .no-data {{
    text-align: center; padding: 3rem;
    color: {C['text_muted']}; font-size: 14px;
  }}

  /* ── Mobile responsiveness ─────────────────────────── */
  @media (max-width: 768px) {{
    .main .block-container {{ padding: 1rem !important; max-width: 100% !important; }}
    .page-header {{ flex-direction: column; align-items: flex-start; gap: 10px; }}
    .page-header-title {{ font-size: 1.15rem !important; }}
    .page-header-sub {{ font-size: 0.75rem !important; }}
    [data-testid="stHorizontalBlock"] {{ flex-wrap: wrap !important; gap: 0.5rem !important; }}
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {{ min-width: 140px !important; flex: 1 1 auto !important; }}
    [data-testid="stMetric"] {{ padding: 0.75rem 1rem !important; }}
    [data-testid="stMetricValue"] {{ font-size: 1.35rem !important; }}
    [data-testid="stMetricLabel"] {{ font-size: 0.65rem !important; }}
    .kpi-band {{ flex-wrap: wrap; gap: 0.5rem; padding: 0.75rem 1rem !important; }}
    .kpi-band-item {{ flex: 1 1 45%; min-width: 120px; border-right: none !important; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 0.5rem 0.25rem !important; }}
    .kpi-band-item:last-child {{ border-bottom: none; }}
    .kpi-band-value {{ font-size: 1.15rem !important; }}
    .em-card {{ padding: 1rem !important; }}
    .section-label {{ margin: 1rem 0 0.5rem !important; font-size: 0.65rem !important; }}
    .metric-grid {{ grid-template-columns: 1fr 1fr !important; gap: 0.5rem !important; }}
    .metric-grid-item {{ padding: 0.75rem 1rem !important; }}
    .metric-grid-value {{ font-size: 1.35rem !important; }}
    .metric-grid-label {{ font-size: 0.65rem !important; }}
    .stTabs [data-baseweb="tab-list"] {{ flex-wrap: wrap !important; }}
    .stTabs [data-baseweb="tab"] {{ padding: 5px 10px !important; font-size: 0.75rem !important; }}
    .funnel-label {{ width: 90px !important; font-size: 11px !important; }}
    .funnel-fill {{ font-size: 10px !important; padding: 0 6px !important; }}
    .insight-row {{ padding: 8px 10px !important; font-size: 12px !important; }}
  }}
</style>
""", unsafe_allow_html=True)



# SVG LINE-ART ICONS (no emoji)

def icon(name, size=16, color="currentColor"):
    icons = {
        "shield":     f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "globe":      f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
        "bar-chart":  f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>',
        "trending":   f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
        "target":     f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        "users":      f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        "zap":        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "pie":        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>',
        "activity":   f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "filter":     f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>',
        "info":       f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
        "cpu":        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
        "calendar":   f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        "map-pin":    f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
        "layers":     f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
        "check":      f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    }
    return icons.get(name, icons["info"])


def card_title(ico, label):
    return f'<p class="em-card-title">{icon(ico, 14, C["primary"])} {label}</p>'



# PLOTLY THEME

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=C["bg"],
    font=dict(family="Inter, Segoe UI, system-ui", color=C["text"], size=11),
    margin=dict(l=10, r=10, t=36, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font_size=10),
    colorway=C["cat"],
    xaxis=dict(gridcolor=C["border"], linecolor=C["border"], showgrid=False),
    yaxis=dict(gridcolor=C["border"], linecolor="rgba(0,0,0,0)", gridwidth=0.5),
    hoverlabel=dict(bgcolor=C["primary_dk"], font_color="white", bordercolor=C["primary"]),
)

def apply_theme(fig, title="", height=360):
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(size=13, color=C["text"]), x=0, xanchor="left"), height=height)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor=C["border"], gridwidth=0.5)
    return fig



# WORLD MAP BUILDER

SADC_COUNTRIES = {
    "Angola", "Botswana", "Comoros", "Democratic Republic of the Congo",
    "Eswatini", "Lesotho", "Madagascar", "Malawi", "Mauritius",
    "Mozambique", "Namibia", "Seychelles", "South Africa",
    "Tanzania", "Zambia", "Zimbabwe",
}

def build_world_map(df):
    ctry = df.groupby("country").agg(
        requests=("client_ip", "count"),
        unique_visitors=("client_ip", "nunique"),
        avg_bytes=("bytes_sent", "mean"),
        error_rate=("status_code", lambda x: (x.isin([404, 500])).mean() * 100),
        conversion_rate=("business_function", lambda x: (x == "Sales_Lead").mean() * 100),
    ).reset_index()

    # Ensure every SADC country appears on the map even if no traffic yet
    missing_sadc = SADC_COUNTRIES - set(ctry["country"])
    if missing_sadc:
        zeros = pd.DataFrame({
            "country": list(missing_sadc),
            "requests": [0] * len(missing_sadc),
            "unique_visitors": [0] * len(missing_sadc),
            "avg_bytes": [0.0] * len(missing_sadc),
            "error_rate": [0.0] * len(missing_sadc),
            "conversion_rate": [0.0] * len(missing_sadc),
        })
        ctry = pd.concat([ctry, zeros], ignore_index=True)

    ctry["sadc"] = ctry["country"].isin(SADC_COUNTRIES)

    fig = go.Figure()

    # Non-SADC base layer (muted slate)
    other = ctry[~ctry["sadc"]]
    if not other.empty:
        fig.add_trace(go.Choropleth(
            locations=other["country"],
            z=other["requests"],
            locationmode="country names",
            colorscale=[[0, "#E9EDF0"], [1, "#9CA3AF"]],
            showscale=False,
            marker_line_color="#FFFFFF",
            marker_line_width=0.5,
            name="Other Markets",
            hovertemplate="<b>%{location}</b><br>Requests: %{z:,}<br>Unique Visitors: %{customdata[0]:,}<extra></extra>",
            customdata=other[["unique_visitors"]].values,
        ))

    # SADC highlight layer (emerald)
    sadc_df = ctry[ctry["sadc"]]
    if not sadc_df.empty:
        fig.add_trace(go.Choropleth(
            locations=sadc_df["country"],
            z=sadc_df["requests"],
            locationmode="country names",
            colorscale=[[0, "#A8D5C7"], [0.5, "#2D9B7A"], [1, "#156450"]],
            colorbar=dict(
                title=dict(text="Requests", side="right", font=dict(size=11, color=C["text"])),
                thickness=12,
                len=0.55,
                x=0.95,
                tickfont=dict(size=10, color=C["text"]),
            ),
            marker_line_color="#D97706",
            marker_line_width=1.5,
            name="SADC Markets",
            hovertemplate="<b>%{location}</b><br>Requests: %{z:,}<br>Unique Visitors: %{customdata[0]:,}<br><b>SADC Member</b><extra></extra>",
            customdata=sadc_df[["unique_visitors"]].values,
        ))

    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#C8D5D1",
        projection_type="natural earth",
        bgcolor="rgba(0,0,0,0)",
        showcountries=True,
        countrycolor="#E9EDF0",
        landcolor="#F8FAF9",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=50, b=0),
        title=dict(
            text="Global Market Presence — SADC Markets Highlighted",
            font=dict(size=13, color=C["text"]),
            x=0.02,
            xanchor="left",
        ),
        height=440,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(size=11, color=C["text"]),
        ),
    )
    return fig, ctry



# AUTHENTICATION

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def show_login():
    st.markdown(f"""
    <style>
      [data-testid="stSidebar"] {{ display: none !important; }}
      .main .block-container {{ padding-top: 6rem !important; max-width: 440px !important; }}
    </style>
    """, unsafe_allow_html=True)

    _, c, _ = st.columns([1, 2.2, 1])
    with c:
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:2rem">
          <div style="width:72px;height:72px;background:{C['primary']};border-radius:16px;display:inline-flex;align-items:center;justify-content:center;margin-bottom:1.5rem">
            {icon("shield", 36, "white")}
          </div>
          <h2 style="margin:0;font-size:1.6rem;color:{C['text']}">CyberNova Analytics</h2>
          <p style="margin:6px 0 0;font-size:0.9rem;color:{C['text_muted']}">Sales Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            st.markdown(f'<p style="font-size:0.7rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:{C["text_muted"]};margin-bottom:1rem">Secure Login</p>', unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter username", key="login_user")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
            submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)

            if submitted:
                if username == "katlegobuka" and password == "kate123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid username or password", icon="🛡")
    st.stop()

if not st.session_state.authenticated:
    show_login()



# DATA LOADING

@st.cache_data(show_spinner="Loading analytics data...")
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    paths = [
        os.path.join(base, "cleaned_logs.csv"),
        os.path.join(base, "data", "cleaned_logs.csv"),
        os.path.join(base, "..", "cybernova_bi_project", "data", "cleaned_logs.csv"),
    ]
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p, parse_dates=["timestamp"])
            df["date"]     = pd.to_datetime(df["date"])
            # Shift Oct 2024 data → Apr 2026
            offset = pd.DateOffset(months=18)
            df["timestamp"] = df["timestamp"] + offset
            df["date"]      = df["date"] + offset
            df["hour"]     = df["timestamp"].dt.hour
            df["week"]     = df["date"].dt.isocalendar().week
            df["month"]    = df["date"].dt.month_name()
            df["day_num"]  = (df["date"] - df["date"].min()).dt.days
            return df
    st.error("Data file not found. Run the pipeline scripts first.")
    st.stop()

df_full = load_data()


# SIDEBAR

with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
      <div class="sb-logo">{icon("shield", 20, "white")}</div>
      <div>
        <p class="sb-title">CyberNova Analytics</p>
        <p class="sb-sub">Sales Intelligence Platform</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<p style="font-size:11px;font-weight:700;letter-spacing:0.1em;opacity:0.7;margin-bottom:6px">{icon("filter",12,"#a8d5c7")} &nbsp;FILTERS</p>', unsafe_allow_html=True)

    all_countries = sorted(df_full["country"].unique())
    sel_countries = st.multiselect("Country", all_countries, default=all_countries, key="country_filter")

    all_services = sorted(df_full["service_category"].unique())
    sel_services = st.multiselect("Service Category", all_services, default=all_services, key="svc_filter")

    dmin = df_full["date"].min().date()
    dmax = df_full["date"].max().date()
    date_range = st.date_input("Date Range", value=(dmin, dmax), min_value=dmin, max_value=dmax)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:11px;font-weight:700;letter-spacing:0.1em;opacity:0.7;margin-bottom:8px">{icon("layers",12,"#a8d5c7")} &nbsp;DATASET</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;color:#a8d5c7;margin:3px 0">{icon("activity",11,"#a8d5c7")} &nbsp;{len(df_full):,} log entries</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;color:#a8d5c7;margin:3px 0">{icon("map-pin",11,"#a8d5c7")} &nbsp;{df_full["country"].nunique()} countries</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;color:#a8d5c7;margin:3px 0">{icon("calendar",11,"#a8d5c7")} &nbsp;30-day period</p>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
# 
# APPLY FILTERS
# 
df = df_full.copy()
if sel_countries:
    df = df[df["country"].isin(sel_countries)]
if sel_services:
    df = df[df["service_category"].isin(sel_services)]
if len(date_range) == 2:
    df = df[(df["date"] >= pd.Timestamp(date_range[0])) & (df["date"] <= pd.Timestamp(date_range[1]))]

N = len(df)

# 
# PAGE HEADER
# 
st.markdown(f"""
<div class="page-header">
  <div class="page-header-logo">{icon("shield", 24, "white")}</div>
  <div>
    <p class="page-header-title">Sales Analytics Dashboard</p>
    <p class="page-header-sub">CyberNova Analytics Ltd - IIS Web Server Log Intelligence</p>
  </div>
</div>
""", unsafe_allow_html=True)


# KPI BAND

total_req    = N
unique_vis   = df["client_ip"].nunique()
conv_rate    = df[df["business_function"] == "Sales_Lead"].shape[0] / max(N, 1) * 100
error_rate   = df[df["status_code"].isin([404, 500])].shape[0] / max(N, 1) * 100
top_country  = df["country"].value_counts().index[0] if N > 0 else "-"
engagement   = N / max(unique_vis, 1)

# Deltas vs full dataset
d_total  = N / max(len(df_full), 1) * 100
d_conv   = conv_rate - (df_full[df_full["business_function"]=="Sales_Lead"].shape[0] / len(df_full) * 100)

metrics_html = ""
for label, value, delta in [
    ("Total Requests",   f"{total_req:,}",    f"{d_total:.0f}% of dataset"),
    ("Unique Visitors",  f"{unique_vis:,}",   f"{unique_vis/max(N,1)*100:.1f}% unique"),
    ("Conversion Rate",  f"{conv_rate:.1f}%", f"{d_conv:+.1f}pp vs full"),
    ("Error Rate",       f"{error_rate:.1f}%","404 + 500 combined"),
    ("Avg Engagement",   f"{engagement:.1f}x","req / visitor"),
    ("Top Market",       top_country,         "by request volume"),
]:
    metrics_html += f"""
    <div class="metric-grid-item">
      <div class="metric-grid-label">{label}</div>
      <div class="metric-grid-value">{value}</div>
      <div class="metric-grid-delta">{delta}</div>
    </div>"""
st.markdown(f'<div class="metric-grid">{metrics_html}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# TABS

tabs = st.tabs([
    "Overview",
    "Geographic Analysis",
    "Service Performance",
    "Traffic Patterns",
    "Predictive Trends",
    "Diagnostics",
])

tab_overview, tab_geo, tab_svc, tab_traffic, tab_pred, tab_diag = tabs



# TAB 1 - OVERVIEW (Executive Summary)

with tab_overview:

    # ── World Map + SADC Summary ──────────────────────────
    st.markdown(f'<p class="section-label">{icon("globe",12,C["primary"])} &nbsp; Global Market Map — SADC Highlighted</p>', unsafe_allow_html=True)

    fig_map, ctry_stats_map = build_world_map(df)
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})

    sadc_present = ctry_stats_map[
        (ctry_stats_map["country"].isin(SADC_COUNTRIES)) &
        (ctry_stats_map["requests"] > 0)
    ].sort_values("requests", ascending=False)
    if not sadc_present.empty:
        st.markdown(f'<p style="font-size:0.75rem;font-weight:700;color:{C["text_muted"]};text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.75rem">SADC Market Performance</p>', unsafe_allow_html=True)
        for start in range(0, len(sadc_present), 4):
            chunk = sadc_present.iloc[start:start+4]
            cols = st.columns(len(chunk))
            for col, (_, row) in zip(cols, chunk.iterrows()):
                with col:
                    st.markdown(f"""
                    <div style="background:{C['white']};border:1px solid {C['border']};border-radius:10px;padding:0.75rem 1rem;text-align:center">
                      <div style="font-size:0.7rem;font-weight:700;color:{C['text_muted']};text-transform:uppercase;letter-spacing:0.06em">{row['country']}</div>
                      <div style="font-size:1.4rem;font-weight:700;color:{C['primary']};margin:4px 0">{row['requests']:,}</div>
                      <div style="font-size:0.7rem;color:{C['text_muted']}">{row['unique_visitors']:,} visitors · {row['conversion_rate']:.1f}% conv</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f'<p class="section-label">{icon("zap",12,C["primary"])} &nbsp; Executive Snapshot</p>', unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        # Daily traffic area + trend
        daily = df.groupby("date").size().reset_index(name="count")
        if len(daily) >= 3:
            daily["day_num"] = (daily["date"] - daily["date"].min()).dt.days
            m = LinearRegression().fit(daily[["day_num"]], daily["count"])
            daily["trend"] = m.predict(daily[["day_num"]])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily["date"], y=daily["count"],
            mode="lines", fill="tozeroy",
            fillcolor=f"rgba(21,100,80,0.12)",
            line=dict(color=C["primary"], width=2.5),
            name="Daily Requests",
            hovertemplate="<b>%{x|%b %d}</b><br>%{y:,} requests<extra></extra>"
        ))
        if len(daily) >= 3:
            fig.add_trace(go.Scatter(
                x=daily["date"], y=daily["trend"],
                mode="lines",
                line=dict(color=C["warning"], width=1.8, dash="dash"),
                name=f"Trend ({m.coef_[0]:+.1f}/day)",
                hovertemplate="Trend: %{y:.0f}<extra></extra>"
            ))
        apply_theme(fig, "Daily Request Volume", 280)
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

        # Service + Business function side by side
        c_a, c_b = st.columns(2)
        with c_a:
            svc_counts = df["service_category"].value_counts().reset_index()
            svc_counts.columns = ["Service", "Count"]
            svc_counts["Service"] = svc_counts["Service"].str.replace("_", " ")
            fig2 = px.bar(svc_counts, x="Count", y="Service", orientation="h",
                          color="Count", color_continuous_scale=["#A8D5C7", C["primary"]],
                          text="Count")
            fig2.update_traces(texttemplate="%{text:,}", textposition="outside", marker_line_width=0)
            fig2.update_coloraxes(showscale=False)
            apply_theme(fig2, "Service Demand", 300)
            fig2.update_layout(yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

        with c_b:
            bf = df["business_function"].value_counts().reset_index()
            bf.columns = ["Function", "Count"]
            fig3 = px.pie(bf, values="Count", names="Function",
                          color_discrete_sequence=C["cat"], hole=0.55)
            fig3.update_traces(textinfo="percent", textfont_size=10,
                               marker=dict(line=dict(color=C["bg"], width=2)))
            apply_theme(fig3, "Business Function", 300)
            fig3.update_layout(legend=dict(orientation="v", x=1.0, y=0.5, font_size=9))
            st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

    with col_right:
        # Funnel
        st.markdown(f'<div class="em-card">{card_title("target","Sales Conversion Funnel")}', unsafe_allow_html=True)
        funnel_data = {
            "Awareness":     df[df["business_function"] == "Awareness"].shape[0],
            "Marketing":     df[df["business_function"] == "Marketing"].shape[0],
            "Product Interest": df[df["business_function"] == "Product_Interest"].shape[0],
            "Sales Lead":    df[df["business_function"] == "Sales_Lead"].shape[0],
            "Support":       df[df["business_function"] == "Service"].shape[0],
        }
        base_val = max(funnel_data.values()) or 1
        shades = ["#A8D5C7", "#5BB89A", "#2D9B7A", C["primary"], C["primary_dk"]]
        rows_html = ""
        for i, (label, val) in enumerate(funnel_data.items()):
            pct = val / base_val * 100
            conv = val / max(N, 1) * 100
            rows_html += f"""
            <div class="funnel-row">
              <span class="funnel-label">{label}</span>
              <div class="funnel-track">
                <div class="funnel-fill" style="width:{pct}%;background:{shades[i]}">{val:,}</div>
              </div>
              <span class="funnel-pct">{conv:.1f}%</span>
            </div>"""
        st.markdown(f'<div class="funnel-wrap">{rows_html}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Status code breakdown
        st.markdown(f'<div class="em-card">{card_title("activity","HTTP Status Overview")}', unsafe_allow_html=True)
        sc = df["status_code"].value_counts().sort_index()
        sc_colors = {200: C["success"], 304: C["primary_lt"], 404: C["warning"], 500: C["danger"]}
        sc_labels = {200: "Success", 304: "Not Modified", 404: "Not Found", 500: "Server Error"}
        for code, cnt in sc.items():
            pct  = cnt / max(N, 1) * 100
            col  = sc_colors.get(code, C["primary"])
            lbl  = sc_labels.get(code, str(code))
            fill = int(pct)
            st.markdown(f"""
            <div style="margin-bottom:9px">
              <div style="display:flex;justify-content:space-between;font-size:11px;color:{C['text_muted']};margin-bottom:3px">
                <span><b style="color:{col}">{code}</b> - {lbl}</span>
                <span>{cnt:,} ({pct:.1f}%)</span>
              </div>
              <div style="background:{C['bg2']};border-radius:4px;height:8px;overflow:hidden">
                <div style="width:{fill}%;background:{col};height:100%;border-radius:4px"></div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# TAB 2 - GEOGRAPHIC ANALYSIS

with tab_geo:

    st.markdown(f'<p class="section-label">{icon("globe",12,C["primary"])} &nbsp; Demographic Segmentation & Regional Performance</p>', unsafe_allow_html=True)

    # Top row: map-style bar + region pie
    c1, c2 = st.columns([3, 2], gap="large")

    with c1:
        geo = df.groupby(["country", "region"]).size().reset_index(name="Requests")
        geo = geo.sort_values("Requests", ascending=True)
        geo["Share"] = (geo["Requests"] / geo["Requests"].sum() * 100).round(1)

        fig = px.bar(geo, x="Requests", y="country", orientation="h",
                     color="region", color_discrete_sequence=C["cat"],
                     text="Share", hover_data={"region": True, "Requests": ":,", "Share": ":.1f"})
        fig.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
        apply_theme(fig, "Request Volume by Country", 360)
        fig.update_layout(legend_title_text="Region", yaxis_title="")
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    with c2:
        region_counts = df["region"].value_counts().reset_index()
        region_counts.columns = ["Region", "Count"]
        fig2 = px.pie(region_counts, values="Count", names="Region",
                      color_discrete_sequence=C["cat"], hole=0.5)
        fig2.update_traces(textinfo="label+percent", textfont_size=10,
                           marker=dict(line=dict(color=C["bg"], width=2)))
        apply_theme(fig2, "Traffic Share by Region", 360)
        st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

    st.markdown(f'<p class="section-label">{icon("bar-chart",12,C["primary"])} &nbsp; Country × Service Cross-Analysis</p>', unsafe_allow_html=True)

    # Grouped bar: service by country
    cross = pd.crosstab(df["country"], df["service_category"]).reset_index()
    cross_m = cross.melt(id_vars="country", var_name="Service", value_name="Requests")
    cross_m["Service"] = cross_m["Service"].str.replace("_", " ")
    # Top 5 services
    top5 = df["service_category"].value_counts().head(5).index
    cross_m = cross_m[cross_m["Service"].isin([s.replace("_"," ") for s in top5])]

    fig3 = px.bar(cross_m, x="country", y="Requests", color="Service",
                  barmode="group", color_discrete_sequence=C["cat"],
                  text_auto=False)
    fig3.update_traces(marker_line_width=0)
    apply_theme(fig3, "Service Requests by Country (Top 5 Services)", 380)
    fig3.update_layout(xaxis_title="", legend_title_text="Service Category")
    st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

    # Country stats table
    st.markdown(f'<p class="section-label">{icon("layers",12,C["primary"])} &nbsp; Country Performance Summary</p>', unsafe_allow_html=True)
    ctry_stats = df.groupby("country").agg(
        Requests=("client_ip", "count"),
        Unique_Visitors=("client_ip", "nunique"),
        Avg_Bytes=("bytes_sent", "mean"),
        Error_Rate=("status_code", lambda x: (x.isin([404,500])).mean() * 100),
        Conversion_Rate=("business_function", lambda x: (x == "Sales_Lead").mean() * 100),
    ).round(2).sort_values("Requests", ascending=False).reset_index()
    ctry_stats.columns = ["Country","Requests","Unique Visitors","Avg Response (B)","Error Rate (%)","Conv. Rate (%)"]
    st.dataframe(ctry_stats, width='stretch', hide_index=True)



# TAB 3 - SERVICE PERFORMANCE

with tab_svc:

    st.markdown(f'<p class="section-label">{icon("bar-chart",12,C["primary"])} &nbsp; Campaign & Service Performance Metrics</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        svc_v = df["service_category"].value_counts().reset_index()
        svc_v.columns = ["Service","Count"]
        svc_v["Service"] = svc_v["Service"].str.replace("_"," ")
        fig = px.bar(svc_v, x="Service", y="Count", color="Count",
                     color_continuous_scale=["#A8D5C7", C["primary"]],
                     text="Count")
        fig.update_traces(texttemplate="%{text:,}", textposition="outside", marker_line_width=0)
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, "Total by Service Category", 320)
        fig.update_layout(xaxis=dict(tickangle=-30))
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    with c2:
        # Error rate by service
        err = df.groupby("service_category").apply(
            lambda x: (x["status_code"].isin([404,500])).mean() * 100
        ).reset_index(name="Error Rate (%)")
        err["service_category"] = err["service_category"].str.replace("_"," ")
        err = err.sort_values("Error Rate (%)", ascending=False)
        err_colors = [C["danger"] if v > 12 else (C["warning"] if v > 8 else C["success"]) for v in err["Error Rate (%)"]]
        fig2 = go.Figure(go.Bar(
            x=err["Error Rate (%)"], y=err["service_category"],
            orientation="h", marker_color=err_colors,
            text=err["Error Rate (%)"].round(1),
            texttemplate="%{text}%", textposition="outside",
        ))
        apply_theme(fig2, "Error Rate by Service", 320)
        fig2.update_layout(yaxis_title="")
        st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

    with c3:
        # Conversion (sales lead) rate by country
        conv = df.groupby("country").apply(
            lambda x: (x["business_function"] == "Sales_Lead").mean() * 100
        ).reset_index(name="Conv Rate (%)")
        conv = conv.sort_values("Conv Rate (%)", ascending=True)
        fig3 = px.bar(conv, x="Conv Rate (%)", y="country", orientation="h",
                      color="Conv Rate (%)", color_continuous_scale=["#E9EDF0", C["primary"]],
                      text="Conv Rate (%)")
        fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside", marker_line_width=0)
        fig3.update_coloraxes(showscale=False)
        apply_theme(fig3, "Conversion Rate by Country", 320)
        fig3.update_layout(yaxis_title="")
        st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

    # Treemap: requests by country > service
    st.markdown(f'<p class="section-label">{icon("layers",12,C["primary"])} &nbsp; Market Segmentation Treemap</p>', unsafe_allow_html=True)
    tree = df.groupby(["region","country","service_category"]).size().reset_index(name="count")
    tree["service_category"] = tree["service_category"].str.replace("_"," ")
    fig4 = px.treemap(tree, path=[px.Constant("All Markets"), "region", "country", "service_category"],
                      values="count", color="count",
                      color_continuous_scale=["#E9EDF0", "#A8D5C7", C["primary"]],
                      color_continuous_midpoint=tree["count"].median())
    fig4.update_traces(textinfo="label+value", marker=dict(line=dict(width=1.5, color=C["bg"])))
    apply_theme(fig4, "Market Segmentation: Region → Country → Service", 500)
    fig4.update_coloraxes(showscale=False)
    st.plotly_chart(fig4, width='stretch', config={"displayModeBar": False})



# TAB 4 - TRAFFIC PATTERNS

with tab_traffic:

    st.markdown(f'<p class="section-label">{icon("activity",12,C["primary"])} &nbsp; Temporal Traffic Patterns</p>', unsafe_allow_html=True)

    # Heatmap: hour × day of week
    c1, c2 = st.columns([3, 2], gap="large")

    with c1:
        df_h = df.copy()
        df_h["dow"] = df_h["timestamp"].dt.dayofweek
        df_h["dow_name"] = df_h["timestamp"].dt.day_name()
        heat = df_h.groupby(["dow_name","hour"]).size().reset_index(name="count")
        heat_pivot = heat.pivot(index="dow_name", columns="hour", values="count").fillna(0)
        order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        heat_pivot = heat_pivot.reindex([d for d in order if d in heat_pivot.index])

        fig = go.Figure(go.Heatmap(
            z=heat_pivot.values, x=heat_pivot.columns, y=heat_pivot.index,
            colorscale=[[0,"#E9EDF0"],[0.5,"#5BB89A"],[1, C["primary_dk"]]],
            hovertemplate="<b>%{y} %{x}:00</b><br>%{z:,} requests<extra></extra>",
            showscale=True, colorbar=dict(thickness=12, len=0.8, title="Requests"),
        ))
        apply_theme(fig, "Traffic Heatmap: Hour of Day × Day of Week", 340)
        fig.update_xaxes(title="Hour of Day", dtick=2)
        fig.update_yaxes(title="")
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    with c2:
        # Hourly bar
        hourly = df.groupby("hour").size().reset_index(name="count")
        bar_colors = [C["primary"] if (9 <= h <= 17) else "#A8D5C7" for h in hourly["hour"]]
        fig2 = go.Figure(go.Bar(
            x=hourly["hour"], y=hourly["count"],
            marker_color=bar_colors, marker_line_width=0,
            hovertemplate="<b>%{x}:00</b> - %{y:,} req<extra></extra>",
        ))
        apply_theme(fig2, "Requests by Hour of Day", 340)
        fig2.update_layout(xaxis=dict(title="Hour", dtick=3))
        fig2.add_annotation(text="Business hours (09–17)", x=13, y=hourly["count"].max(),
                            showarrow=False, font=dict(size=9, color=C["text_muted"]))
        st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

    # Day-of-week + top pages
    c3, c4 = st.columns([2, 3], gap="large")

    with c3:
        dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        wkly = df.groupby(["date","day_of_week"]).size().reset_index(name="count")
        wkly_avg = wkly.groupby("day_of_week")["count"].mean().reindex(dow_order).dropna().reset_index()
        wkly_avg.columns = ["Day","Avg Requests"]
        wday_colors = [C["primary"] if d not in ["Saturday","Sunday"] else C["warning"] for d in wkly_avg["Day"]]
        fig3 = go.Figure(go.Bar(
            x=wkly_avg["Day"], y=wkly_avg["Avg Requests"],
            marker_color=wday_colors, marker_line_width=0,
            text=wkly_avg["Avg Requests"].round(0),
            texttemplate="%{text:.0f}", textposition="outside",
        ))
        apply_theme(fig3, "Average Requests by Day of Week", 320)
        fig3.update_layout(xaxis=dict(tickangle=-20))
        st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

    with c4:
        # Top 12 pages
        top_pages = df["url"].value_counts().head(12).reset_index()
        top_pages.columns = ["URL","Requests"]
        top_pages = top_pages.sort_values("Requests", ascending=True)
        fig4 = px.bar(top_pages, x="Requests", y="URL", orientation="h",
                      color="Requests", color_continuous_scale=["#A8D5C7", C["primary"]],
                      text="Requests")
        fig4.update_traces(texttemplate="%{text:,}", textposition="outside", marker_line_width=0)
        fig4.update_coloraxes(showscale=False)
        apply_theme(fig4, "Top 12 Requested Endpoints", 320)
        fig4.update_layout(yaxis_title="")
        st.plotly_chart(fig4, width='stretch', config={"displayModeBar": False})

    # Response size distribution
    st.markdown(f'<p class="section-label">{icon("activity",12,C["primary"])} &nbsp; Response Size Distribution</p>', unsafe_allow_html=True)
    fig5 = go.Figure()
    fig5.add_trace(go.Histogram(
        x=df["bytes_sent"], nbinsx=60,
        marker_color=C["primary"], marker_line_width=0.3,
        marker_line_color=C["bg"], opacity=0.85,
        hovertemplate="Range: %{x:,}<br>Count: %{y:,}<extra></extra>",
        name="Frequency",
    ))
    fig5.add_vline(x=df["bytes_sent"].mean(), line_width=2, line_dash="dash",
                   line_color=C["warning"], annotation_text=f"Mean {df['bytes_sent'].mean():,.0f}B",
                   annotation_font_color=C["warning"])
    fig5.add_vline(x=df["bytes_sent"].median(), line_width=2, line_dash="dot",
                   line_color=C["danger"], annotation_text=f"Median {df['bytes_sent'].median():,.0f}B",
                   annotation_font_color=C["danger"], annotation_position="top left")
    apply_theme(fig5, "Response Size (bytes_sent) Distribution", 280)
    fig5.update_layout(xaxis_title="Bytes Sent", yaxis_title="Frequency", showlegend=False)
    st.plotly_chart(fig5, width='stretch', config={"displayModeBar": False})



# TAB 5 - PREDICTIVE TRENDS

with tab_pred:

    st.markdown(f'<p class="section-label">{icon("trending",12,C["primary"])} &nbsp; Revenue-KPI Trend Forecasting & Predictive Models</p>', unsafe_allow_html=True)

    daily = df.groupby("date").size().reset_index(name="count")

    if len(daily) < 5:
        st.warning("Insufficient data for predictions. Expand the date filter.")
    else:
        daily["day_num"] = (daily["date"] - daily["date"].min()).dt.days
        model = LinearRegression().fit(daily[["day_num"]], daily["count"])
        r2    = model.score(daily[["day_num"]], daily["count"])
        daily["trend"] = model.predict(daily[["day_num"]])

        # 14-day forecast
        last_day  = daily["day_num"].max()
        last_date = daily["date"].max()
        f_days    = np.arange(last_day + 1, last_day + 15)
        f_dates   = [last_date + pd.Timedelta(days=int(i)) for i in range(1, 15)]
        f_vals    = model.predict(f_days.reshape(-1, 1))
        f_lower   = f_vals * 0.87
        f_upper   = f_vals * 1.13

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Model R²",          f"{r2:.4f}", "Goodness of fit")
        m2.metric("Trend Slope",       f"{model.coef_[0]:+.2f}", "Requests/day")
        m3.metric("14-Day Avg Forecast", f"{f_vals.mean():.0f}", "Projected daily")
        growth_pct = (f_vals.mean() - daily["count"].tail(7).mean()) / max(daily["count"].tail(7).mean(), 1) * 100
        m4.metric("Growth Projection", f"{growth_pct:+.1f}%", "vs last 7 days")

        # Main forecast chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily["date"], y=daily["count"], name="Actual",
            mode="lines+markers", marker=dict(size=4, color=C["primary"]),
            line=dict(color=C["primary"], width=2),
            fill="tozeroy", fillcolor="rgba(21,100,80,0.08)",
            hovertemplate="<b>%{x|%b %d}</b><br>%{y:,} req<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=daily["date"], y=daily["trend"], name="Trend Line",
            mode="lines", line=dict(color=C["warning"], width=2, dash="dash"),
            hovertemplate="Trend: %{y:.0f}<extra></extra>",
        ))
        # Confidence band
        fig.add_trace(go.Scatter(
            x=f_dates + f_dates[::-1],
            y=list(f_upper) + list(f_lower[::-1]),
            fill="toself", fillcolor="rgba(220,38,38,0.1)",
            line=dict(color="rgba(0,0,0,0)"), name="±13% CI", showlegend=True,
        ))
        fig.add_trace(go.Scatter(
            x=f_dates, y=f_vals, name="14-Day Forecast",
            mode="lines+markers", marker=dict(size=5, color=C["danger"]),
            line=dict(color=C["danger"], width=2.5),
            hovertemplate="<b>%{x|%b %d}</b><br>Forecast: %{y:.0f}<extra></extra>",
        ))
        fig.add_shape(type="line", x0=last_date, x1=last_date, y0=0, y1=1,
                      yref="paper", line=dict(width=1.5, dash="dot", color=C["border"]))
        fig.add_annotation(x=last_date, y=1, yref="paper", text="  Forecast →",
                           showarrow=False, font=dict(color=C["text_muted"], size=10),
                           xanchor="left", yanchor="top")
        apply_theme(fig, f"Traffic Forecast - Linear Regression (R² = {r2:.4f})", 380)
        fig.update_layout(xaxis_title="Date", yaxis_title="Daily Requests")
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

        c1, c2 = st.columns([2, 3], gap="large")

        with c1:
            # Forecast table
            st.markdown(f'<div class="em-card">{card_title("calendar","14-Day Forecast Table")}', unsafe_allow_html=True)
            fdf = pd.DataFrame({
                "Date":       [str(d.date()) for d in f_dates],
                "Predicted":  f_vals.round(0).astype(int),
                "Low (−13%)": f_lower.round(0).astype(int),
                "High (+13%)":f_upper.round(0).astype(int),
            })
            st.dataframe(fdf, width='stretch', hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            # Service growth per-service linear regression
            st.markdown(f'<p class="section-label">{icon("trending",12,C["primary"])} &nbsp; Service Growth Rates</p>', unsafe_allow_html=True)
            svc_daily = df.groupby(["date","service_category"]).size().reset_index(name="count")
            svc_daily["day_num"] = (svc_daily["date"] - svc_daily["date"].min()).dt.days
            growth_rows = []
            for svc, grp in svc_daily.groupby("service_category"):
                if len(grp) < 5: continue
                sm = LinearRegression().fit(grp[["day_num"]], grp["count"])
                growth_rows.append({
                    "Service": svc.replace("_"," "),
                    "Slope (req/day)": round(float(sm.coef_[0]), 3),
                    "R²": round(float(sm.score(grp[["day_num"]], grp["count"])), 4),
                    "Signal": "Growing" if sm.coef_[0] > 0.05 else ("Declining" if sm.coef_[0] < -0.05 else "Stable"),
                })
            gdf = pd.DataFrame(growth_rows).sort_values("Slope (req/day)", ascending=False)
            fig2 = px.bar(gdf, x="Slope (req/day)", y="Service", orientation="h",
                          color="Signal",
                          color_discrete_map={"Growing": C["success"], "Stable": C["primary_lt"], "Declining": C["danger"]},
                          text="Slope (req/day)")
            fig2.update_traces(texttemplate="%{text:+.3f}", textposition="outside", marker_line_width=0)
            apply_theme(fig2, "Service Growth Slope (req/day)", 360)
            fig2.update_layout(yaxis_title="", legend_title_text="Trend")
            st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

        # Country growth
        st.markdown(f'<p class="section-label">{icon("map-pin",12,C["primary"])} &nbsp; Country-Level Growth Trends</p>', unsafe_allow_html=True)
        ctry_daily = df.groupby(["date","country"]).size().reset_index(name="count")
        ctry_daily["day_num"] = (ctry_daily["date"] - ctry_daily["date"].min()).dt.days
        fig3 = px.line(ctry_daily, x="date", y="count", color="country",
                       color_discrete_sequence=C["cat"],
                       hover_data={"date": "|%b %d", "count": ":,", "country": True})
        apply_theme(fig3, "Daily Request Volume by Country", 360)
        fig3.update_layout(xaxis_title="Date", yaxis_title="Requests", legend_title_text="Country")
        fig3.update_traces(line_width=1.8)
        st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})



# TAB 6 - DIAGNOSTICS

with tab_diag:

    st.markdown(f'<p class="section-label">{icon("cpu",12,C["primary"])} &nbsp; Diagnostic Analysis - Weak Point Identification</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")

    with c1:
        # Error heatmap by country × service
        err_cross = df.copy()
        err_cross["is_error"] = err_cross["status_code"].isin([404, 500]).astype(int)
        err_pivot = err_cross.groupby(["country","service_category"])["is_error"].mean() * 100
        err_pivot = err_pivot.unstack(fill_value=0).round(1)
        err_pivot.columns = [c.replace("_"," ") for c in err_pivot.columns]

        fig = go.Figure(go.Heatmap(
            z=err_pivot.values, x=err_pivot.columns, y=err_pivot.index,
            colorscale=[[0,"#E9EDF0"],[0.5,C["warning"]],[1,C["danger"]]],
            hovertemplate="<b>%{y} × %{x}</b><br>Error rate: %{z:.1f}%<extra></extra>",
            showscale=True, colorbar=dict(thickness=12, title="Err %"),
        ))
        apply_theme(fig, "Error Rate Heatmap: Country × Service (%)", 380)
        fig.update_layout(xaxis=dict(tickangle=-30))
        st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    with c2:
        # Referrer source breakdown
        ref = df["referrer"].value_counts().reset_index()
        ref.columns = ["Referrer","Count"]
        ref["Referrer"] = ref["Referrer"].replace("-","Direct")
        fig2 = px.pie(ref.head(8), values="Count", names="Referrer",
                      color_discrete_sequence=C["cat"], hole=0.45)
        fig2.update_traces(textinfo="percent+label", textfont_size=9,
                           marker=dict(line=dict(color=C["bg"], width=2)))
        apply_theme(fig2, "Traffic by Referrer Source", 380)
        st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

    st.markdown(f'<p class="section-label">{icon("activity",12,C["primary"])} &nbsp; Underperforming Segments</p>', unsafe_allow_html=True)

    c3, c4 = st.columns(2, gap="large")

    with c3:
        # Engagement depth: avg requests per unique IP by country
        eng = df.groupby("country").apply(
            lambda x: len(x) / x["client_ip"].nunique()
        ).reset_index(name="Engagement Depth")
        eng = eng.sort_values("Engagement Depth", ascending=True)
        avg_eng = eng["Engagement Depth"].mean()
        eng["Flag"] = eng["Engagement Depth"].apply(
            lambda x: "Below Average" if x < avg_eng else "Above Average"
        )
        fig3 = px.bar(eng, x="Engagement Depth", y="country", orientation="h",
                      color="Flag",
                      color_discrete_map={"Below Average": C["warning"], "Above Average": C["success"]},
                      text="Engagement Depth")
        fig3.update_traces(texttemplate="%{text:.2f}x", textposition="outside", marker_line_width=0)
        fig3.add_vline(x=avg_eng, line_dash="dash", line_color=C["primary"],
                       annotation_text=f"Avg {avg_eng:.2f}x")
        apply_theme(fig3, "Engagement Depth by Country (req/visitor)", 340)
        fig3.update_layout(yaxis_title="", legend_title_text="Performance")
        st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

    with c4:
        # User agent distribution
        ua = df["user_agent"].value_counts().reset_index()
        ua.columns = ["Agent","Count"]
        ua["Agent"] = ua["Agent"].str.slice(0, 45) + "..."
        fig4 = px.bar(ua.head(7), x="Count", y="Agent", orientation="h",
                      color="Count", color_continuous_scale=["#A8D5C7", C["primary"]],
                      text="Count")
        fig4.update_traces(texttemplate="%{text:,}", textposition="outside", marker_line_width=0)
        fig4.update_coloraxes(showscale=False)
        apply_theme(fig4, "User Agent Distribution", 340)
        fig4.update_layout(yaxis_title="")
        st.plotly_chart(fig4, width='stretch', config={"displayModeBar": False})

    # Full diagnostic stats table
    st.markdown(f'<p class="section-label">{icon("layers",12,C["primary"])} &nbsp; Full Descriptive Statistics</p>', unsafe_allow_html=True)
    diag_stats = df.groupby("service_category").agg(
        Total_Requests=("client_ip","count"),
        Unique_IPs=("client_ip","nunique"),
        Avg_Bytes=("bytes_sent","mean"),
        Median_Bytes=("bytes_sent","median"),
        Error_Rate_pct=("status_code", lambda x: (x.isin([404,500])).mean()*100),
        Conv_Rate_pct=("business_function", lambda x: (x=="Sales_Lead").mean()*100),
        Peak_Hour=("hour", lambda x: x.mode().iloc[0] if len(x)>0 else 0),
    ).round(2).reset_index()
    diag_stats.columns = ["Service","Requests","Unique IPs","Avg Bytes","Median Bytes","Error %","Conv %","Peak Hour"]
    st.dataframe(diag_stats, width='stretch', hide_index=True)


# FOOTER

st.markdown(f"""
<div style="margin-top:3rem;padding-top:1rem;border-top:1px solid {C['border']};
     display:flex;justify-content:center;align-items:center;
     font-size:11px;color:{C['text_muted']}">
  <span>{icon('shield',12,C['text_muted'])} &nbsp; CyberNova Analytics Ltd - Sales Intelligence Dashboard</span>
</div>
""", unsafe_allow_html=True)

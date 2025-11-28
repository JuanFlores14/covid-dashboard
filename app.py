import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="COVID-19 Vaccination Impact Analysis",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Editorial/Data Journalism aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* Base styles */
    .stApp {
        background-color: #FAFAF8 !important;
    }

    html, body, [class*="css"], .main, .block-container {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #1a1a1a !important;
    }

    /* Force sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #fff !important;
        border-right: 1px solid #e0e0e0 !important;
    }

    section[data-testid="stSidebar"] .stRadio > label {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.9rem !important;
        color: #1a1a1a !important;
    }
    
    /* Main header - editorial style */
    .main-header {
        font-family: 'Source Serif 4', Georgia, serif !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: #1a1a1a !important;
        text-align: left !important;
        padding: 0 0 10px 0 !important;
        margin-bottom: 10px !important;
        border-bottom: 3px solid #1a1a1a !important;
        letter-spacing: -0.5px !important;
        line-height: 1.15 !important;
    }

    /* Subheader */
    .sub-header {
        font-family: 'Source Serif 4', Georgia, serif !important;
        font-size: 1.75rem !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
        margin-top: 48px !important;
        margin-bottom: 20px !important;
        letter-spacing: -0.3px !important;
    }

    /* Byline/credit line */
    .byline {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.95rem !important;
        color: #666 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 28px !important;
    }

    /* Lead paragraph */
    .lead-text {
        font-family: 'Source Serif 4', Georgia, serif !important;
        font-size: 1.4rem !important;
        line-height: 1.75 !important;
        color: #2a2a2a !important;
        max-width: 720px !important;
        margin-bottom: 36px !important;
    }
    
    /* Metric cards - minimal style */
    .metric-card {
        background-color: #fff !important;
        padding: 28px 24px !important;
        border: 1px solid #e0e0e0 !important;
        position: relative !important;
    }

    .metric-card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 3px !important;
        background-color: #1e3a5f !important;
    }

    .metric-label {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: #666 !important;
        margin-bottom: 10px !important;
    }

    .metric-value {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 2.1rem !important;
        font-weight: 500 !important;
        color: #1a1a1a !important;
    }
    
    /* Insight box - editorial callout */
    .insight-box {
        background-color: #fff;
        padding: 24px 28px;
        border-left: 4px solid #1e3a5f;
        margin: 28px 0;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    .insight-box p {
        margin: 0;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #333;
    }
    
    .insight-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #1e3a5f;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    /* Story section cards */
    .story-card {
        background: #fff;
        border: 1px solid #e0e0e0;
        padding: 28px;
        height: 100%;
    }
    
    .story-number {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        color: #999;
        margin-bottom: 10px;
    }
    
    .story-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 10px;
    }
    
    .story-desc {
        font-size: 1rem;
        color: #666;
        line-height: 1.6;
    }
    
    /* Adoption category cards */
    .category-card {
        padding: 28px;
        border: 1px solid #e0e0e0;
        background: #fff;
    }
    
    .category-early {
        border-top: 4px solid #2d6a4f;
    }
    
    .category-mid {
        border-top: 4px solid #b08968;
    }
    
    .category-late {
        border-top: 4px solid #9d4b4b;
    }
    
    .category-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }
    
    .category-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2.4rem;
        font-weight: 500;
        margin-bottom: 6px;
    }
    
    .category-period {
        font-size: 0.95rem;
        color: #666;
    }
    
    /* Recommendation cards */
    .rec-card {
        background: #fff;
        border: 1px solid #e0e0e0;
        padding: 28px;
        margin-bottom: 20px;
    }
    
    .rec-number {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.9rem;
        color: #1e3a5f;
        margin-bottom: 10px;
    }
    
    .rec-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 14px;
    }
    
    .rec-text {
        font-size: 1rem;
        line-height: 1.7;
        color: #444;
    }
    
    .rec-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888;
        margin-top: 14px;
    }
    
    /* Timeline cards */
    .timeline-card {
        padding: 24px 28px;
        border: 1px solid #e0e0e0;
        background: #fff;
        text-align: center;
    }
    
    .timeline-period {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #1e3a5f;
        margin-bottom: 10px;
    }
    
    .timeline-range {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.25rem;
        font-weight: 500;
        margin-bottom: 14px;
    }
    
    .timeline-items {
        font-size: 0.95rem;
        color: #666;
        line-height: 1.7;
    }
    
    /* Final message box */
    .final-box {
        background: #1e3a5f;
        color: #fff;
        padding: 48px;
        margin: 48px 0;
    }
    
    .final-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.75rem;
        font-weight: 600;
        margin-bottom: 20px;
    }
    
    .final-text {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.25rem;
        line-height: 1.8;
        opacity: 0.95;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #fff;
        border-right: 1px solid #e0e0e0;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
    }
    
    /* Remove default streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Plotly chart styling adjustments */
    .stPlotlyChart {
        background: #fff;
        border: 1px solid #e0e0e0;
        padding: 16px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Footer */
    .footer {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.8rem;
        color: #888;
        text-align: center;
        padding: 32px 0;
        border-top: 1px solid #e0e0e0;
        margin-top: 48px;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Color palette for charts - Updated with accent colors for key countries
COLORS = {
    'primary': '#1e3a5f',
    'secondary': '#c76b4a',
    'early': '#2d6a4f',
    'mid': '#b08968',
    'late': '#9d4b4b',
    'neutral': '#666666',
    'light': '#e0e0e0',
    'background': '#FAFAF8',
    # Accent colors for highlighting
    'mexico': '#c41e3a',      # Carmesí - destacar México
    'usa': '#1e5aa8',         # Azul intenso - destacar USA
    'success': '#1d7a5f',     # Verde azulado - países con buena correlación
    'muted': '#d0d0d0',       # Gris claro para países no destacados
}

# Plotly template
CHART_TEMPLATE = {
    'layout': {
        'font': {'family': 'IBM Plex Sans, sans-serif', 'color': '#1a1a1a'},
        'paper_bgcolor': '#fff',
        'plot_bgcolor': '#FAFAF8',
        'title': {'font': {'family': 'Source Serif 4, Georgia, serif', 'size': 16, 'color': '#1a1a1a'}},
    }
}

# Load data
@st.cache_data
def load_data():
    merged_data = pd.read_csv('covid_analysis_data.csv')
    merged_data['Vaccine_Intro_Date'] = pd.to_datetime(merged_data['Vaccine_Intro_Date'])
    
    time_series = pd.read_csv('covid_time_series.csv')
    time_series['date'] = pd.to_datetime(time_series['date'])
    
    deaths_by_age = pd.read_csv('covid_deaths_by_age.csv')
    
    return merged_data, time_series, deaths_by_age

merged_data, time_series, deaths_by_age = load_data()

# Sidebar
st.sidebar.markdown("""
<div style='padding: 16px 0 24px 0; border-bottom: 1px solid #e0e0e0; margin-bottom: 24px;'>
    <div style='font-family: Source Serif 4, Georgia, serif; font-size: 1.1rem; font-weight: 600; color: #1a1a1a;'>
        COVID-19 Analysis
    </div>
    <div style='font-size: 0.75rem; color: #888; margin-top: 4px;'>
        Vaccination Impact Study
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigate",
    ["Executive Summary", "The Crisis", "The Solution", "The Evidence", "Recommendations"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size: 0.8rem; color: #666; line-height: 1.6;'>
    <div style='font-weight: 600; margin-bottom: 8px;'>About this Analysis</div>
    <p><strong>Role:</strong> Healthcare Data Analyst</p>
    <p><strong>Audience:</strong> Secretary of Health</p>
    <p><strong>Focus:</strong> Vaccine timing and mortality outcomes</p>
</div>
""", unsafe_allow_html=True)

# ==================== PAGE 1: EXECUTIVE SUMMARY ====================
if page == "Executive Summary":
    st.markdown('<h1 class="main-header">The Race Against Time</h1>', unsafe_allow_html=True)
    st.markdown('<p class="byline">COVID-19 Vaccination Impact Analysis</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="lead-text">
        This analysis examines data from 130 countries to answer a critical question from the pandemic: 
        Did countries that adopted vaccines earlier experience different mortality outcomes?
    </p>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Countries Analyzed</div>
            <div class="metric-value">130</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_deaths = merged_data['Total_Deaths'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Deaths</div>
            <div class="metric-value">{total_deaths:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        earliest_vax = merged_data['Vaccine_Intro_Date'].min().strftime('%b %d, %Y')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">First Vaccination</div>
            <div class="metric-value" style="font-size: 1.3rem;">{earliest_vax}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        latest_vax = merged_data['Vaccine_Intro_Date'].max().strftime('%b %d, %Y')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Last to Adopt</div>
            <div class="metric-value" style="font-size: 1.3rem;">{latest_vax}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="sub-header">Structure of Analysis</h2>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    sections = [
        ("01", "The Crisis", "Understanding the scale and demographic impact of COVID-19 mortality"),
        ("02", "The Solution", "When and how countries introduced vaccination programs"),
        ("03", "The Evidence", "Statistical analysis of timing versus outcomes"),
        ("04", "Recommendations", "Strategic implications for future pandemic preparedness")
    ]
    
    for col, (num, title, desc) in zip(cols, sections):
        with col:
            st.markdown(f"""
            <div class="story-card">
                <div class="story-number">{num}</div>
                <div class="story-title">{title}</div>
                <div class="story-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== PAGE 2: THE CRISIS ====================
elif page == "The Crisis":
    st.markdown('<h1 class="main-header">Understanding the Impact</h1>', unsafe_allow_html=True)
    st.markdown('<p class="byline">COVID-19 Mortality Patterns</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="lead-text">
        Before vaccines arrived, COVID-19 devastated populations worldwide. Understanding who was 
        affected—and where—is essential context for evaluating vaccination strategies.
    </p>
    """, unsafe_allow_html=True)
    
    # Total deaths by country
    st.markdown('<h2 class="sub-header">Global Death Toll by Country</h2>', unsafe_allow_html=True)
    
    top_20_deaths = merged_data.nlargest(20, 'Total_Deaths').sort_values('Total_Deaths', ascending=True)
    
    # Create color array to highlight Mexico and USA
    bar_colors = []
    for country in top_20_deaths['Country']:
        if country == 'Mexico':
            bar_colors.append(COLORS['mexico'])
        elif country == 'United States of America':
            bar_colors.append(COLORS['usa'])
        else:
            bar_colors.append(COLORS['muted'])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_20_deaths['Total_Deaths'],
        y=top_20_deaths['Country'],
        orientation='h',
        marker_color=bar_colors,
        text=top_20_deaths['Total_Deaths'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside',
        textfont=dict(family='IBM Plex Mono', size=12, color='#555'),
        showlegend=False
    ))
    
    fig.update_layout(
        xaxis_title='Total Deaths',
        yaxis_title=None,
        height=580,
        font=dict(family='IBM Plex Sans', size=12),
        paper_bgcolor='#fff',
        plot_bgcolor='#FAFAF8',
        xaxis=dict(gridcolor='#e0e0e0', showline=True, linecolor='#e0e0e0'),
        yaxis=dict(showline=False, tickfont=dict(size=12)),
        margin=dict(l=0, r=60, t=20, b=40),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Legend for highlighted countries
    st.markdown(f"""
    <div style='display: flex; gap: 32px; margin-bottom: 20px; font-size: 0.9rem;'>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 16px; height: 16px; background: {COLORS['usa']}; border-radius: 2px;'></div>
            <span>United States</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 16px; height: 16px; background: {COLORS['mexico']}; border-radius: 2px;'></div>
            <span>Mexico</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 16px; height: 16px; background: {COLORS['muted']}; border-radius: 2px;'></div>
            <span>Other countries</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-label">Key Finding</div>
        <p>The United States recorded over 1.2 million deaths, followed by Brazil with 289,000 and Mexico with 279,000. 
        These three countries alone account for a significant portion of global COVID-19 mortality, 
        though population size is a major factor in absolute numbers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Deaths by age group
    st.markdown('<h2 class="sub-header">Demographic Vulnerability</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        age_totals = deaths_by_age.groupby('Agegroup')['Deaths'].sum().reset_index()
        age_totals['Percentage'] = (age_totals['Deaths'] / age_totals['Deaths'].sum() * 100).round(1)
        age_totals = age_totals.sort_values('Deaths', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6.5))
        
        # Use a refined color gradient with more contrast
        n_bars = len(age_totals)
        colors = plt.cm.Blues(np.linspace(0.35, 0.85, n_bars))[::-1]
        
        bars = ax.barh(age_totals['Agegroup'], age_totals['Deaths'], color=colors)
        
        for i, (deaths, pct) in enumerate(zip(age_totals['Deaths'], age_totals['Percentage'])):
            ax.text(deaths + age_totals['Deaths'].max() * 0.02, i, 
                   f'{deaths:,.0f} ({pct}%)', 
                   va='center', fontsize=11, fontfamily='IBM Plex Mono', color='#444')
        
        ax.set_xlabel('Total Deaths', fontsize=12, fontfamily='IBM Plex Sans', color='#555')
        ax.set_ylabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#e0e0e0')
        ax.spines['left'].set_visible(False)
        ax.tick_params(colors='#555', labelsize=11)
        ax.set_facecolor('#FAFAF8')
        fig.patch.set_facecolor('#fff')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="insight-box" style="margin-top: 0;">
            <div class="insight-label">Critical Pattern</div>
            <p>The elderly population (65+) bore a disproportionate mortality burden. 
            This demographic reality shaped vaccination prioritization strategies globally.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Top 3 age groups summary
        for i, (_, row) in enumerate(age_totals.head(3).iterrows()):
            st.markdown(f"""
            <div style='padding: 12px 16px; background: #fff; border: 1px solid #e0e0e0; margin-bottom: 8px;'>
                <div style='font-family: IBM Plex Mono; font-size: 0.8rem; color: #888;'>#{i+1}</div>
                <div style='font-weight: 600; margin: 4px 0;'>{row['Agegroup']}</div>
                <div style='font-family: IBM Plex Mono; color: #1e3a5f;'>{row['Percentage']}% of deaths</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== PAGE 3: THE SOLUTION ====================
elif page == "The Solution":
    st.markdown('<h1 class="main-header">Vaccine Introduction Timeline</h1>', unsafe_allow_html=True)
    st.markdown('<p class="byline">Global Adoption Patterns</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="lead-text">
        Vaccines became available at different times across countries. This section examines 
        adoption patterns and the factors that influenced rollout speed.
    </p>
    """, unsafe_allow_html=True)
    
    # Key statistics - USA and Mexico ranking
    st.markdown('<h2 class="sub-header">Adoption Sequence</h2>', unsafe_allow_html=True)

    timeline_data = merged_data.sort_values('Vaccine_Intro_Date').reset_index(drop=True)
    timeline_data['Rank'] = timeline_data.index + 1
    timeline_data['Category'] = pd.cut(
        timeline_data['Vaccine_Intro_Date'],
        bins=[pd.Timestamp('2020-01-01'), pd.Timestamp('2021-02-01'),
              pd.Timestamp('2021-05-01'), pd.Timestamp('2022-01-01')],
        labels=['Early Adopters', 'Mid Adopters', 'Late Adopters']
    )

    # Get USA and Mexico data
    usa_rank = timeline_data[timeline_data['Country'] == 'United States of America'].iloc[0]
    mexico_rank = timeline_data[timeline_data['Country'] == 'Mexico'].iloc[0]
    total_countries = len(timeline_data)

    # Display key stats
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style='background: {COLORS['usa']}; padding: 32px 28px; border: 1px solid #e0e0e0; text-align: center;'>
            <div style='font-family: IBM Plex Sans; font-size: 0.9rem; text-transform: uppercase;
                        letter-spacing: 1.5px; color: rgba(255,255,255,0.9); margin-bottom: 12px;'>
                United States
            </div>
            <div style='font-family: IBM Plex Mono; font-size: 3rem; font-weight: 600;
                        color: #fff; margin-bottom: 8px;'>
                #{usa_rank['Rank']}
            </div>
            <div style='font-size: 1.1rem; color: rgba(255,255,255,0.95); margin-bottom: 4px;'>
                de {total_countries} países
            </div>
            <div style='font-family: IBM Plex Mono; font-size: 0.95rem; color: rgba(255,255,255,0.85);'>
                {usa_rank['Vaccine_Intro_Date'].strftime('%B %d, %Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background: {COLORS['mexico']}; padding: 32px 28px; border: 1px solid #e0e0e0; text-align: center;'>
            <div style='font-family: IBM Plex Sans; font-size: 0.9rem; text-transform: uppercase;
                        letter-spacing: 1.5px; color: rgba(255,255,255,0.9); margin-bottom: 12px;'>
                México
            </div>
            <div style='font-family: IBM Plex Mono; font-size: 3rem; font-weight: 600;
                        color: #fff; margin-bottom: 8px;'>
                #{mexico_rank['Rank']}
            </div>
            <div style='font-size: 1.1rem; color: rgba(255,255,255,0.95); margin-bottom: 4px;'>
                de {total_countries} países
            </div>
            <div style='font-family: IBM Plex Mono; font-size: 0.95rem; color: rgba(255,255,255,0.85);'>
                {mexico_rank['Vaccine_Intro_Date'].strftime('%B %d, %Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

    # World map visualization
    map_data = timeline_data.copy()

    fig = px.choropleth(
        map_data,
        locations='Country_code',
        color='Category',
        hover_name='Country',
        hover_data={
            'Country_code': False,
            'Vaccine_Intro_Date': '|%B %d, %Y',
            'Rank': True,
            'Category': True
        },
        color_discrete_map={
            'Early Adopters': COLORS['early'],
            'Mid Adopters': COLORS['mid'],
            'Late Adopters': COLORS['late']
        },
        category_orders={'Category': ['Early Adopters', 'Mid Adopters', 'Late Adopters']},
        labels={'Vaccine_Intro_Date': 'Adoption Date', 'Rank': 'Ranking'}
    )

    fig.update_layout(
        height=550,
        font=dict(family='IBM Plex Sans', size=12),
        paper_bgcolor='#fff',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#e0e0e0',
            projection_type='natural earth',
            bgcolor='#FAFAF8',
            landcolor='#f5f5f5',
            oceancolor='#FAFAF8'
        ),
        legend=dict(
            title=dict(text='Adoption Category', font=dict(size=12, family='IBM Plex Sans')),
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
        margin=dict(l=0, r=0, t=20, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Category statistics
    st.markdown('<h2 class="sub-header">Adoption Categories</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    early_count = len(timeline_data[timeline_data['Category'] == 'Early Adopters'])
    mid_count = len(timeline_data[timeline_data['Category'] == 'Mid Adopters'])
    late_count = len(timeline_data[timeline_data['Category'] == 'Late Adopters'])

    # Usar contenedores con estilo para cada categoría
    with col1:
        st.container()
        st.markdown(f"""
        <div style='background: #fff; padding: 20px; border-left: 4px solid {COLORS['early']};
                    border-right: 1px solid #e0e0e0; border-top: 1px solid #e0e0e0;
                    border-bottom: 1px solid #e0e0e0; margin-bottom: 10px;'>
            <p style='color: {COLORS['early']}; font-size: 0.75rem; font-weight: 600;
                      text-transform: uppercase; letter-spacing: 1px; margin: 0;'>Early Adopters</p>
        </div>
        """, unsafe_allow_html=True)
        st.metric(label="Countries", value=early_count, label_visibility="collapsed")
        st.markdown(f"""
        <div style='background: #fff; padding: 10px 20px; border-left: 4px solid {COLORS['early']};
                    border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
            <p style='color: #666; font-size: 0.9rem; margin: 0;'>Before February 2021</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.container()
        st.markdown(f"""
        <div style='background: #fff; padding: 20px; border-left: 4px solid {COLORS['mid']};
                    border-right: 1px solid #e0e0e0; border-top: 1px solid #e0e0e0;
                    border-bottom: 1px solid #e0e0e0; margin-bottom: 10px;'>
            <p style='color: {COLORS['mid']}; font-size: 0.75rem; font-weight: 600;
                      text-transform: uppercase; letter-spacing: 1px; margin: 0;'>Mid Adopters</p>
        </div>
        """, unsafe_allow_html=True)
        st.metric(label="Countries", value=mid_count, label_visibility="collapsed")
        st.markdown(f"""
        <div style='background: #fff; padding: 10px 20px; border-left: 4px solid {COLORS['mid']};
                    border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
            <p style='color: #666; font-size: 0.9rem; margin: 0;'>February – May 2021</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.container()
        st.markdown(f"""
        <div style='background: #fff; padding: 20px; border-left: 4px solid {COLORS['late']};
                    border-right: 1px solid #e0e0e0; border-top: 1px solid #e0e0e0;
                    border-bottom: 1px solid #e0e0e0; margin-bottom: 10px;'>
            <p style='color: {COLORS['late']}; font-size: 0.75rem; font-weight: 600;
                      text-transform: uppercase; letter-spacing: 1px; margin: 0;'>Late Adopters</p>
        </div>
        """, unsafe_allow_html=True)
        st.metric(label="Countries", value=late_count, label_visibility="collapsed")
        st.markdown(f"""
        <div style='background: #fff; padding: 10px 20px; border-left: 4px solid {COLORS['late']};
                    border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
            <p style='color: #666; font-size: 0.9rem; margin: 0;'>After May 2021</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box" style="margin-top: 32px;">
        <div class="insight-label">Observation</div>
        <p>97% of analyzed countries had introduced vaccines by May 2021. 
        However, timing differences of even a few months had implications for mortality outcomes during peak waves.</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== PAGE 4: THE EVIDENCE ====================
elif page == "The Evidence":
    st.markdown('<h1 class="main-header">Analyzing the Relationship</h1>', unsafe_allow_html=True)
    st.markdown('<p class="byline">Vaccine Timing and Mortality Outcomes</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="lead-text">
        The central question: Did countries that adopted vaccines earlier experience fewer deaths? 
        The answer is more nuanced than a simple correlation might suggest.
    </p>
    """, unsafe_allow_html=True)
    
    # Main scatter plot
    st.markdown('<h2 class="sub-header">Timing vs. Total Deaths</h2>', unsafe_allow_html=True)
    
    plot_data = merged_data.copy()
    plot_data['Category'] = pd.cut(
        plot_data['Vaccine_Intro_Date'],
        bins=[pd.Timestamp('2020-01-01'), pd.Timestamp('2021-02-01'), 
              pd.Timestamp('2021-05-01'), pd.Timestamp('2022-01-01')],
        labels=['Early Adopters', 'Mid Adopters', 'Late Adopters']
    )
    
    # Identify success stories: early adopters with relatively low deaths
    early_adopters = plot_data[plot_data['Category'] == 'Early Adopters'].copy()
    death_threshold = early_adopters['Total_Deaths'].quantile(0.25)  # Bottom 25% of early adopters
    
    # Create highlight categories
    def get_highlight_category(row):
        if row['Country'] == 'Mexico':
            return 'Mexico'
        elif row['Country'] == 'United States of America':
            return 'United States'
        elif row['Category'] == 'Early Adopters' and row['Total_Deaths'] <= death_threshold:
            return 'Early + Low Deaths'
        else:
            return 'Other'
    
    plot_data['Highlight'] = plot_data.apply(get_highlight_category, axis=1)
    
    # Custom scatter plot with highlighting
    fig = go.Figure()
    
    # Plot "Other" countries first (background, muted)
    other_data = plot_data[plot_data['Highlight'] == 'Other']
    fig.add_trace(go.Scatter(
        x=other_data['Vaccine_Intro_Date'],
        y=other_data['Total_Deaths'],
        mode='markers',
        name='Other countries',
        marker=dict(
            size=other_data['Total_Deaths'].apply(lambda x: max(8, min(30, np.log10(x+1) * 6))),
            color=COLORS['muted'],
            opacity=0.5,
            line=dict(width=1, color='#fff')
        ),
        text=other_data['Country'],
        hovertemplate='<b>%{text}</b><br>Deaths: %{y:,.0f}<br>Date: %{x|%b %d, %Y}<extra></extra>'
    ))
    
    # Plot success stories (early adopters with low deaths)
    success_data = plot_data[plot_data['Highlight'] == 'Early + Low Deaths']
    fig.add_trace(go.Scatter(
        x=success_data['Vaccine_Intro_Date'],
        y=success_data['Total_Deaths'],
        mode='markers',
        name='Early adopters, low mortality',
        marker=dict(
            size=12,
            color=COLORS['success'],
            symbol='diamond',
            line=dict(width=2, color='#fff')
        ),
        text=success_data['Country'],
        hovertemplate='<b>%{text}</b><br>Deaths: %{y:,.0f}<br>Date: %{x|%b %d, %Y}<extra></extra>'
    ))
    
    # Plot Mexico (highlighted)
    mexico_data = plot_data[plot_data['Highlight'] == 'Mexico']
    fig.add_trace(go.Scatter(
        x=mexico_data['Vaccine_Intro_Date'],
        y=mexico_data['Total_Deaths'],
        mode='markers+text',
        name='Mexico',
        marker=dict(
            size=22,
            color=COLORS['mexico'],
            symbol='circle',
            line=dict(width=2, color='#fff')
        ),
        text=['Mexico'],
        textposition='top center',
        textfont=dict(size=12, color=COLORS['mexico'], family='IBM Plex Sans'),
        hovertemplate='<b>Mexico</b><br>Deaths: %{y:,.0f}<br>Date: %{x|%b %d, %Y}<extra></extra>'
    ))
    
    # Plot USA (highlighted)
    usa_data = plot_data[plot_data['Highlight'] == 'United States']
    fig.add_trace(go.Scatter(
        x=usa_data['Vaccine_Intro_Date'],
        y=usa_data['Total_Deaths'],
        mode='markers+text',
        name='United States',
        marker=dict(
            size=28,
            color=COLORS['usa'],
            symbol='circle',
            line=dict(width=2, color='#fff')
        ),
        text=['United States'],
        textposition='top center',
        textfont=dict(size=12, color=COLORS['usa'], family='IBM Plex Sans'),
        hovertemplate='<b>United States</b><br>Deaths: %{y:,.0f}<br>Date: %{x|%b %d, %Y}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Vaccine Introduction Date',
        yaxis_title='Total Deaths (log scale)',
        yaxis_type="log",
        height=600,
        font=dict(family='IBM Plex Sans', size=12),
        paper_bgcolor='#fff',
        plot_bgcolor='#FAFAF8',
        legend=dict(
            title=dict(text=''),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11)
        ),
        xaxis=dict(gridcolor='#e0e0e0', tickfont=dict(size=11)),
        yaxis=dict(gridcolor='#e0e0e0', tickfont=dict(size=11)),
        margin=dict(l=0, r=20, t=50, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Custom legend explanation
    st.markdown(f"""
    <div style='display: flex; flex-wrap: wrap; gap: 24px; margin: 16px 0 24px 0; font-size: 0.95rem;'>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 18px; height: 18px; background: {COLORS['usa']}; border-radius: 50%;'></div>
            <span><strong>United States</strong> — highest absolute deaths</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 18px; height: 18px; background: {COLORS['mexico']}; border-radius: 50%;'></div>
            <span><strong>Mexico</strong> — third highest deaths</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <div style='width: 14px; height: 14px; background: {COLORS['success']}; transform: rotate(45deg);'></div>
            <span style='margin-left: 4px;'><strong>Success cases</strong> — early adoption + low mortality</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-label">Important Context</div>
        <p>The scatter reveals a complex picture: while USA and Mexico (both early adopters) show high death counts, 
        this reflects population size and pandemic severity. The green diamonds highlight countries that achieved 
        both early vaccine adoption AND relatively low mortality — these represent potential models for effective 
        pandemic response strategies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics by category
    st.markdown('<h2 class="sub-header">Mortality by Adoption Category</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        category_stats = plot_data.groupby('Category').agg({
            'Total_Deaths': ['mean', 'median', 'count']
        }).round(0)
        category_stats.columns = ['Mean', 'Median', 'Count']
        category_stats = category_stats.reset_index()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
        
        colors = [COLORS['early'], COLORS['mid'], COLORS['late']]
        x_pos = np.arange(len(category_stats))
        
        # Mean deaths
        bars1 = ax1.bar(x_pos, category_stats['Mean'], color=colors, width=0.6)
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(['Early', 'Mid', 'Late'], fontsize=12)
        ax1.set_ylabel('Average Deaths', fontsize=12, color='#555')
        ax1.set_title('Mean Deaths', fontsize=14, fontweight='500', fontfamily='IBM Plex Sans', pad=14)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_color('#e0e0e0')
        ax1.spines['left'].set_color('#e0e0e0')
        ax1.set_facecolor('#FAFAF8')
        ax1.tick_params(axis='y', labelsize=11)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1000,
                    f'{height:,.0f}', ha='center', va='bottom', 
                    fontsize=11, fontfamily='IBM Plex Mono', color='#444')
        
        # Median deaths
        bars2 = ax2.bar(x_pos, category_stats['Median'], color=colors, width=0.6)
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(['Early', 'Mid', 'Late'], fontsize=12)
        ax2.set_ylabel('Median Deaths', fontsize=12, color='#555')
        ax2.set_title('Median Deaths', fontsize=14, fontweight='500', fontfamily='IBM Plex Sans', pad=14)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_color('#e0e0e0')
        ax2.spines['left'].set_color('#e0e0e0')
        ax2.set_facecolor('#FAFAF8')
        ax2.tick_params(axis='y', labelsize=11)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{height:,.0f}', ha='center', va='bottom',
                    fontsize=11, fontfamily='IBM Plex Mono', color='#444')
        
        fig.patch.set_facecolor('#fff')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        for _, row in category_stats.iterrows():
            color = {'Early Adopters': COLORS['early'], 
                    'Mid Adopters': COLORS['mid'], 
                    'Late Adopters': COLORS['late']}[row['Category']]
            st.markdown(f"""
            <div style='padding: 20px; margin: 10px 0; background: #fff; 
                        border-left: 4px solid {color}; border: 1px solid #e0e0e0;'>
                <div style='font-weight: 600; color: {color}; font-size: 1rem;'>{row['Category']}</div>
                <div style='margin-top: 10px; font-size: 0.95rem; color: #555; line-height: 1.7;'>
                    <span style='font-family: IBM Plex Mono;'>{row['Count']:.0f}</span> countries<br>
                    Mean: <span style='font-family: IBM Plex Mono;'>{row['Mean']:,.0f}</span><br>
                    Median: <span style='font-family: IBM Plex Mono;'>{row['Median']:,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box" style="margin-top: 24px;">
        <div class="insight-label">Statistical Nuance</div>
        <p>Early adopters show higher mean deaths (skewed by large countries), but median values 
        tell a different story. Population size, pandemic wave timing, and healthcare capacity 
        are significant confounding factors.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Regional heatmap
    st.markdown('<h2 class="sub-header">Regional Patterns</h2>', unsafe_allow_html=True)

    regional_data = plot_data.groupby(['Who_region', 'Category'])['Total_Deaths'].mean().reset_index()
    pivot_data = regional_data.pivot(index='Who_region', columns='Category', values='Total_Deaths')

    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.heatmap(pivot_data, annot=False,
                cmap='Blues', cbar_kws={'label': 'Average Deaths'},
                linewidths=3, linecolor='#fff', ax=ax)

    # Agregar texto manualmente sobre cada celda
    for i in range(len(pivot_data)):
        for j in range(len(pivot_data.columns)):
            value = pivot_data.iloc[i, j]
            if not pd.isna(value):
                # Color blanco para AMR-Early Adopters (celda más oscura)
                region = pivot_data.index[i]
                category = pivot_data.columns[j]
                text_color = '#ffffff' if (region == 'AMR' and category == 'Early Adopters') else '#1a1a1a'

                text = ax.text(j + 0.5, i + 0.5, f'{value:.0f}',
                             ha='center', va='center',
                             fontfamily='IBM Plex Mono', fontsize=14,
                             fontweight='600', color=text_color)

    ax.set_title('')
    ax.set_xlabel('Adoption Category', fontsize=12, color='#555')
    ax.set_ylabel('WHO Region', fontsize=12, color='#555')
    ax.tick_params(labelsize=11)
    ax.set_facecolor('#FAFAF8')
    fig.patch.set_facecolor('#fff')
    plt.tight_layout()
    st.pyplot(fig)

# ==================== PAGE 5: CONSIDERATIONS & NEXT STEPS ====================
elif page == "Recommendations":
    st.markdown('<h1 class="main-header">Considerations & Next Steps</h1>', unsafe_allow_html=True)
    st.markdown('<p class="byline">Interpreting the Evidence</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="lead-text">
        This analysis reveals complex patterns but does not establish clear causation between 
        vaccine adoption timing and mortality outcomes. The following considerations acknowledge 
        both what we learned and what requires further investigation.
    </p>
    """, unsafe_allow_html=True)
    
    # Evidence Gaps - What we cannot conclude
    st.markdown('<h2 class="sub-header">What We Cannot Conclude</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box" style="border-left-color: #9d4b4b;">
        <div class="insight-label" style="color: #9d4b4b;">Evidence Gaps</div>
        <p style="margin-bottom: 16px;">
            <strong>Correlation ≠ Causation:</strong> Early vaccine adoption did not consistently predict lower mortality. 
            Countries like the USA and Brazil adopted early but had high death counts due to population size and other factors.
        </p>
        <p style="margin-bottom: 16px;">
            <strong>Confounding variables dominate:</strong> Population size, healthcare infrastructure quality, 
            pandemic wave timing, reporting standards, and socioeconomic conditions all significantly 
            influenced outcomes — often more than adoption timing itself.
        </p>
        <p>
            <strong>Data limitations:</strong> Absolute death counts without population normalization 
            make direct country comparisons misleading. The analysis supports general preparedness principles 
            but cannot validate specific timing thresholds.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key findings - keeping this section
    st.markdown('<h2 class="sub-header">Summary of Findings</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #fff; padding: 28px; border: 1px solid #e0e0e0;'>
            <div style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; color: #2d6a4f; margin-bottom: 14px;'>
                What the Data Shows
            </div>
            <ul style='margin: 0; padding-left: 20px; line-height: 1.9; color: #444; font-size: 1rem;'>
                <li>130 countries analyzed with complete data</li>
                <li>60 countries achieved early adoption</li>
                <li>65+ age group bore disproportionate mortality</li>
                <li>Regional variations in both timing and outcomes</li>
                <li>Population size was a major confounding factor</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #fff; padding: 28px; border: 1px solid #e0e0e0;'>
            <div style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; color: #b08968; margin-bottom: 14px;'>
                Limitations & Context
            </div>
            <ul style='margin: 0; padding-left: 20px; line-height: 1.9; color: #444; font-size: 1rem;'>
                <li>Large countries had more deaths regardless of timing</li>
                <li>Pandemic waves occurred at different times globally</li>
                <li>Healthcare infrastructure varied significantly</li>
                <li>Reporting quality differed between countries</li>
                <li>Socioeconomic factors played major roles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Further Research Needed
    st.markdown('<h2 class="sub-header">Further Research Needed</h2>', unsafe_allow_html=True)
    
    research_items = [
        {
            "num": "01",
            "title": "Population-Normalized Analysis",
            "desc": "Conduct analysis using deaths per 100,000 population to enable meaningful cross-country comparisons and control for size effects."
        },
        {
            "num": "02",
            "title": "Controlled Regional Comparisons",
            "desc": "Compare countries with similar demographics, healthcare systems, and pandemic timing but different adoption speeds to isolate the vaccine timing variable."
        },
        {
            "num": "03",
            "title": "Qualitative Decision-Maker Research",
            "desc": "Survey health officials to understand barriers to faster adoption — supply constraints, regulatory processes, or distribution challenges."
        }
    ]
    
    for item in research_items:
        st.markdown(f"""
        <div style='background: #fff; padding: 24px 28px; border: 1px solid #e0e0e0; margin-bottom: 16px; border-left: 3px solid #1e3a5f;'>
            <div style='font-family: IBM Plex Mono; font-size: 0.85rem; color: #1e3a5f; margin-bottom: 8px;'>{item['num']}</div>
            <div style='font-family: Source Serif 4, Georgia, serif; font-size: 1.15rem; font-weight: 600; margin-bottom: 10px;'>{item['title']}</div>
            <div style='font-size: 1rem; line-height: 1.7; color: #444;'>{item['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Preliminary Considerations (formerly Priority Actions) - reduced to 3
    st.markdown('<h2 class="sub-header">Preliminary Considerations</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p style='font-size: 1rem; color: #666; margin-bottom: 24px; line-height: 1.7;'>
        While further research is needed for definitive conclusions, general pandemic preparedness 
        principles suggest the following areas merit attention:
    </p>
    """, unsafe_allow_html=True)
    
    recommendations = [
        {
            "num": "01",
            "title": "Build Strategic Vaccine Reserves",
            "what": "Establish emergency stockpiles with flexible manufacturing partnerships",
            "why": "Early adopters were those with pre-existing infrastructure and procurement agreements",
            "action": "Allocate budget for reserve capacity and advance purchase agreements"
        },
        {
            "num": "02",
            "title": "Invest in Distribution Infrastructure",
            "what": "Develop cold-chain logistics and last-mile delivery capabilities",
            "why": "Speed of rollout, not just availability, determined success",
            "action": "Map vulnerable populations and pre-position distribution networks"
        },
        {
            "num": "03",
            "title": "Implement Accelerated Approval Protocols",
            "what": "Create frameworks for emergency use authorization",
            "why": "Every week of delay meant preventable deaths",
            "action": "Establish clear criteria and streamlined review processes"
        }
    ]
    
    for rec in recommendations:
        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-number">{rec['num']}</div>
            <div class="rec-title">{rec['title']}</div>
            <div class="rec-text">{rec['what']}</div>
            <div class="rec-label">Rationale</div>
            <div class="rec-text">{rec['why']}</div>
            <div class="rec-label">Action Item</div>
            <div class="rec-text">{rec['action']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Final message - more measured tone
    st.markdown("""
    <div class="final-box">
        <div class="final-title">The Bottom Line</div>
        <div class="final-text">
            This analysis does not provide definitive evidence that early vaccine adoption 
            directly caused lower mortality — the relationship is far more complex than 
            a simple timing correlation.
            <br><br>
            However, the data does support the value of <strong>preparedness infrastructure</strong>: 
            countries that could act quickly had systems already in place. Further research 
            with normalized data and controlled comparisons is essential before drawing 
            policy conclusions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Methodology
    with st.expander("Data Sources & Methodology"):
        st.markdown("""
        **Data Sources**
        
        WHO COVID-19 Data Repository, COVID-19 Vaccination Uptake Data (2021-2023), 
        WHO Global Monthly Death by Age Data, COVID-19 Vaccine Production Data
        
        **Analysis Period**
        
        Deaths: January 2020 – August 2025 | Vaccinations: December 2020 – December 2023
        
        **Methodology**
        
        Total deaths calculated by summing all monthly deaths per country. Vaccine introduction 
        date taken as first recorded vaccination. Countries categorized into Early (before Feb 2021), 
        Mid (Feb-May 2021), and Late (after May 2021) adopters.
        
        **Limitations**
        
        Data quality varies by country. Population size not normalized in some visualizations. 
        Pandemic timing differed globally. Healthcare infrastructure disparities not accounted for.
        """)

# Footer
st.markdown("""
<div class="footer">
    <div>COVID-19 Vaccination Impact Analysis</div>
    <div style='margin-top: 4px;'>Data Source: WHO COVID-19 Data Repository | Analysis Period: 2020–2023</div>
</div>
""", unsafe_allow_html=True)

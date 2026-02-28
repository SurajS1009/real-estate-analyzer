"""
India Land Rate Analyzer & Predictor
==========================================
Comprehensive tool covering ALL 28 States + 8 Union Territories.
Built with Streamlit, Plotly, scikit-learn.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_option_menu import option_menu

from data_module import (
    get_land_rate_data, get_all_states, get_cities_in_state,
    get_development_factors, get_location_insights,
    get_legal_risk_profile, get_area_risk_alerts,
    get_areas_in_city, get_area_details, get_all_area_details,
)
from prediction_engine import (
    predict_future_rates, calculate_investment_roi,
    get_development_forecast, compare_locations,
)

# ─── Page Config ───
st.set_page_config(
    page_title="India Land Rate Analyzer",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    .block-container { padding-top: 1.2rem; font-family: 'Inter', sans-serif; }

    /* Hero */
    .hero-wrap {
        text-align: center; padding: 2.5rem 1rem 1.8rem;
        background: linear-gradient(135deg, rgba(255,107,53,0.06) 0%, rgba(247,201,72,0.04) 100%);
        border-radius: 20px; margin-bottom: 2rem;
    }
    .main-header {
        font-size: 2.6rem; font-weight: 800; letter-spacing: -0.5px;
        background: linear-gradient(135deg, #FF6B35 0%, #e85d26 50%, #F7C948 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
    }
    .sub-header { font-size: 1.05rem; color: #c5cdd7; margin-bottom: 0; font-weight: 400; }
    .hero-badge {
        display: inline-block; margin-top: 1rem;
        background: rgba(255,107,53,0.1); color: #FF6B35; font-size: 0.78rem; font-weight: 600;
        padding: 0.35rem 1rem; border-radius: 20px; letter-spacing: 0.3px;
    }

    /* Sidebar – Always dark for readability in any theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    section[data-testid="stSidebar"] * { color: #f0f0f0 !important; }
    section[data-testid="stSidebar"] .stRadio label span { color: #f0f0f0 !important; font-weight: 500; }
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"] span { color: #FF6B35 !important; font-weight: 700; }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMetric label,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h2 { color: #ffffff !important; }
    section[data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] { color: #FF6B35 !important; }
    section[data-testid="stSidebar"] .stMetric { background: rgba(255,107,53,0.1) !important; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"],
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="popover"] {
        background: rgba(255,255,255,0.12) !important;
        border-color: rgba(255,255,255,0.25) !important;
    }
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] * { color: #ffffff !important; }
    /* Selectbox input & search field */
    section[data-testid="stSidebar"] .stSelectbox input,
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="input"] input,
    section[data-testid="stSidebar"] .stSelectbox [role="combobox"] input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #FF6B35 !important;
        background: transparent !important;
    }
    /* Selectbox placeholder text */
    section[data-testid="stSidebar"] .stSelectbox input::placeholder {
        color: rgba(255,255,255,0.5) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.5) !important;
    }
    /* Dropdown menu list */
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="menu"],
    section[data-testid="stSidebar"] .stSelectbox ul[role="listbox"],
    section[data-testid="stSidebar"] [data-baseweb="popover"] [data-baseweb="menu"] {
        background: #1e2a3a !important;
    }
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="menu"] li,
    section[data-testid="stSidebar"] .stSelectbox ul[role="listbox"] li,
    section[data-testid="stSidebar"] [data-baseweb="popover"] li {
        color: #f0f0f0 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="menu"] li:hover,
    section[data-testid="stSidebar"] .stSelectbox ul[role="listbox"] li:hover,
    section[data-testid="stSidebar"] [data-baseweb="popover"] li:hover,
    section[data-testid="stSidebar"] [data-baseweb="popover"] li[aria-selected="true"] {
        background: rgba(255,107,53,0.2) !important;
        color: #ffffff !important;
    }
    /* Global popover dropdown fix (Streamlit renders popovers outside sidebar) */
    [data-baseweb="popover"] {
        background: #1e2a3a !important;
    }
    [data-baseweb="popover"] [data-baseweb="menu"] {
        background: #1e2a3a !important;
    }
    [data-baseweb="popover"] [data-baseweb="menu"] li {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    [data-baseweb="popover"] [data-baseweb="menu"] li:hover,
    [data-baseweb="popover"] [data-baseweb="menu"] li[aria-selected="true"] {
        background: rgba(255,107,53,0.25) !important;
        color: #ffffff !important;
    }
    [data-baseweb="popover"] input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #FF6B35 !important;
        background: rgba(255,255,255,0.1) !important;
    }
    [data-baseweb="popover"] input::placeholder {
        color: rgba(255,255,255,0.5) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.5) !important;
    }
    ul[role="listbox"] {
        background: #1e2a3a !important;
    }
    ul[role="listbox"] li {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    ul[role="listbox"] li:hover {
        background: rgba(255,107,53,0.25) !important;
    }
    section[data-testid="stSidebar"] svg { color: #f0f0f0 !important; fill: #f0f0f0 !important; }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #f0f0f0 !important; }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4 { color: #ffffff !important; }
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #ffffff !important; }
    /* Nuclear override: ALL sidebar text white */
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] option,
    section[data-testid="stSidebar"] [class*="css"] {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    /* Global: any popover/dropdown — dark bg so white text is readable */
    [data-baseweb="popover"] [data-baseweb="input"] {
        background: rgba(255,255,255,0.1) !important;
    }

    /* Feature Cards */
    .feat-card {
        background: rgba(255,255,255,0.035); padding: 1.5rem 1.2rem 1.3rem; border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.07); text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .feat-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(255,107,53,0.12); }
    .feat-icon {
        width: 52px; height: 52px; border-radius: 14px; margin: 0 auto 0.9rem;
        display: flex; align-items: center; justify-content: center; font-size: 1.5rem;
    }
    .feat-title { font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #FF6B35; letter-spacing: -0.2px; }
    .feat-desc  { font-size: 0.82rem; color: #c5cdd7; line-height: 1.45; }

    /* Step Cards */
    .step-card {
        background: rgba(255,255,255,0.03); padding: 1.6rem; border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.06); text-align: left;
        transition: transform 0.2s ease;
    }
    .step-card:hover { transform: translateY(-3px); }
    .step-num {
        display: inline-flex; align-items: center; justify-content: center;
        width: 34px; height: 34px; border-radius: 10px; font-weight: 800; font-size: 0.9rem;
        margin-right: 0.7rem; flex-shrink: 0;
    }
    .step-title { font-weight: 600; font-size: 1rem; color: #ffffff; }
    .step-desc  { margin-top: 0.7rem; color: #c5cdd7; font-size: 0.88rem; line-height: 1.5; }

    /* Section Headers */
    .section-hdr {
        font-size: 1.3rem; font-weight: 700; color: #FF6B35; margin-bottom: 0.3rem; letter-spacing: -0.3px;
    }
    .section-sub { font-size: 0.88rem; color: #b0b8c4; margin-bottom: 1.4rem; }

    /* Stat Pills */
    .stat-row { display: flex; gap: 0.8rem; justify-content: center; flex-wrap: wrap; margin: 1.2rem 0 0.5rem; }
    .stat-pill {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px; padding: 0.7rem 1.3rem; text-align: center; min-width: 150px;
    }
    .stat-val  { font-size: 1.4rem; font-weight: 800; color: #FF6B35; }
    .stat-label { font-size: 0.78rem; color: #b0b8c4; margin-top: 0.15rem; font-weight: 500; }

    .stMetric { background: rgba(255,107,53,0.05); border-radius: 12px; padding: 0.8rem; }

    /* Weather Widget */
    .weather-card {
        background: linear-gradient(135deg, rgba(14,165,233,0.15) 0%, rgba(56,189,248,0.08) 100%);
        border: 1px solid rgba(14,165,233,0.25); border-radius: 14px;
        padding: 0.9rem 1rem; text-align: center; margin-bottom: 0.5rem;
    }
    .weather-top { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 0.3rem; }
    .weather-temp { font-size: 1.6rem; font-weight: 800; color: #38bdf8 !important; }
    .weather-cond { font-size: 0.82rem; color: #c5cdd7 !important; font-weight: 500; margin-bottom: 0.4rem; }
    .weather-details { display: flex; justify-content: space-around; font-size: 0.72rem; color: #9ca3af !important; }
    .weather-detail-item { text-align: center; }
    .weather-detail-val { font-weight: 700; color: #e0e0e0 !important; font-size: 0.78rem; }
    .aqi-badge {
        display: inline-block; font-size: 0.72rem; font-weight: 700; padding: 0.2rem 0.6rem;
        border-radius: 6px; margin-top: 0.4rem; letter-spacing: 0.3px;
    }

    /* Climate Card */
    .climate-card {
        background: rgba(255,255,255,0.035); padding: 1.2rem 1.4rem; border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
    }
    .climate-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin-top: 0.8rem;
    }
    .climate-item-label { font-size: 0.72rem; color: #8b95a5; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .climate-item-val { font-size: 0.95rem; font-weight: 700; color: #e0e0e0; margin-top: 0.1rem; }
    .climate-note {
        margin-top: 0.9rem; padding: 0.7rem 1rem; border-radius: 10px;
        background: rgba(255,107,53,0.06); border-left: 3px solid #FF6B35;
        font-size: 0.82rem; color: #c5cdd7; line-height: 1.5;
    }
    @media (max-width: 480px) {
        .climate-grid { grid-template-columns: 1fr; }
    }

    /* ── Mobile / Tablet Responsive ── */
    @media (max-width: 768px) {
        .block-container { padding-top: 0.6rem; padding-left: 0.8rem; padding-right: 0.8rem; }

        .hero-wrap { padding: 1.5rem 0.8rem 1.2rem; border-radius: 14px; margin-bottom: 1.2rem; }
        .main-header { font-size: 1.6rem; }
        .sub-header { font-size: 0.88rem; }
        .hero-badge { font-size: 0.7rem; padding: 0.3rem 0.8rem; }

        .stat-row { gap: 0.5rem; }
        .stat-pill { min-width: 120px; padding: 0.5rem 0.8rem; }
        .stat-val { font-size: 1.1rem; }
        .stat-label { font-size: 0.7rem; }

        .section-hdr { font-size: 1.1rem; }
        .section-sub { font-size: 0.8rem; margin-bottom: 1rem; }

        .feat-card { padding: 1.1rem 0.9rem 1rem; border-radius: 12px; }
        .feat-icon { width: 42px; height: 42px; border-radius: 10px; font-size: 1.2rem; margin-bottom: 0.6rem; }
        .feat-title { font-size: 0.88rem; }
        .feat-desc { font-size: 0.76rem; }

        .step-card { padding: 1.1rem; border-radius: 12px; }
        .step-num { width: 28px; height: 28px; font-size: 0.8rem; border-radius: 8px; }
        .step-title { font-size: 0.9rem; }
        .step-desc { font-size: 0.8rem; }

        /* Force Streamlit columns to stack vertically on mobile */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            min-width: 45% !important; flex: 1 1 45% !important;
        }
    }

    @media (max-width: 480px) {
        .main-header { font-size: 1.35rem; }
        .sub-header { font-size: 0.82rem; }
        .hero-badge { font-size: 0.65rem; }

        .stat-pill { min-width: 100px; padding: 0.4rem 0.6rem; }
        .stat-val { font-size: 0.95rem; }

        .feat-card { padding: 0.9rem 0.7rem; }
        .feat-icon { width: 36px; height: 36px; font-size: 1rem; }

        /* Stack to single column on very small screens */
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            min-width: 100% !important; flex: 1 1 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ───
@st.cache_data
def load_data():
    return get_land_rate_data()

@st.cache_data
def load_dev_factors():
    return get_development_factors()

df = load_data()
dev_factors = load_dev_factors()

# ─── Weather Helper ───
WEATHER_API_KEY = "984134a80ec345c1a63120041251209"

@st.cache_data(ttl=600)  # cache 10 minutes
def fetch_weather(city: str):
    """Fetch current weather + AQI from WeatherAPI.com. Returns dict or None."""
    try:
        url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city},India&aqi=yes"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            c = data["current"]
            loc = data["location"]
            # AQI data (US EPA Index: 1=Good, 2=Moderate, 3=Unhealthy-SG, 4=Unhealthy, 5=VeryUnhealthy, 6=Hazardous)
            aqi_raw = c.get("air_quality", {})
            epa = aqi_raw.get("us-epa-index", None)
            pm25 = aqi_raw.get("pm2_5", None)
            pm10 = aqi_raw.get("pm10", None)
            aqi_labels = {1: ("Good", "#22c55e"), 2: ("Moderate", "#eab308"), 3: ("Unhealthy (SG)", "#f97316"),
                          4: ("Unhealthy", "#ef4444"), 5: ("Very Unhealthy", "#a855f7"), 6: ("Hazardous", "#7f1d1d")}
            aqi_label, aqi_color = aqi_labels.get(epa, ("N/A", "#94a3b8"))
            return {
                "temp_c": c["temp_c"],
                "feels": c["feelslike_c"],
                "humidity": c["humidity"],
                "wind_kph": c["wind_kph"],
                "condition": c["condition"]["text"],
                "icon": c["condition"]["icon"],
                "uv": c.get("uv", None),
                "city": loc["name"],
                "region": loc["region"],
                "aqi_epa": epa,
                "aqi_label": aqi_label,
                "aqi_color": aqi_color,
                "pm25": pm25,
                "pm10": pm10,
            }
    except Exception:
        pass
    return None

# ─── Climate Summary Data ───
CITY_CLIMATE = {
    # City: (climate_type, avg_temp_c, avg_rainfall_mm, best_months, worst_months, humidity_range, notes)
    "Mumbai": ("Tropical Wet", 27.2, 2167, "Nov–Feb", "Jun–Sep", "60–90%", "Heavy monsoon; coastal humidity year-round; pleasant winters."),
    "New Delhi": ("Humid Subtropical", 25.0, 797, "Oct–Mar", "May–Jul", "30–80%", "Extreme summers (45°C+); cold winters; monsoon Jul–Sep; AQI concerns in winter."),
    "Bengaluru": ("Tropical Savanna", 23.5, 970, "Sep–Feb", "Mar–May", "45–75%", "Pleasant year-round; moderate monsoon; known as Garden City."),
    "Hyderabad": ("Tropical Wet & Dry", 26.6, 812, "Oct–Feb", "Apr–Jun", "40–75%", "Hot summers; moderate monsoon; pleasant winters."),
    "Chennai": ("Tropical Wet & Dry", 28.6, 1400, "Dec–Feb", "Apr–Jun", "60–85%", "Northeast monsoon Oct–Dec; hot & humid summers; cyclone-prone."),
    "Kolkata": ("Tropical Wet & Dry", 26.8, 1582, "Oct–Mar", "May–Jul", "55–90%", "Hot & humid; heavy monsoon; pleasant winters; occasional cyclones."),
    "Pune": ("Tropical Wet & Dry", 25.0, 722, "Oct–Feb", "Apr–Jun", "35–75%", "Pleasant climate; moderate monsoon; cooler than Mumbai."),
    "Ahmedabad": ("Hot Semi-arid", 27.0, 782, "Nov–Feb", "Apr–Jun", "25–70%", "Very hot summers (45°C+); low rainfall; dry & dusty."),
    "Jaipur": ("Hot Semi-arid", 25.5, 650, "Oct–Mar", "May–Jul", "25–65%", "Desert proximity; extreme summer heat; chilly winters; limited rainfall."),
    "Lucknow": ("Humid Subtropical", 25.8, 896, "Oct–Mar", "May–Jul", "35–80%", "Hot summers; foggy winters; monsoon Jul–Sep."),
    "Chandigarh": ("Humid Subtropical", 23.5, 1110, "Oct–Mar", "May–Jul", "30–75%", "Planned city; cold winters; hot summers; good monsoon."),
    "Chandigarh City": ("Humid Subtropical", 23.5, 1110, "Oct–Mar", "May–Jul", "30–75%", "Planned city; cold winters; hot summers; good monsoon."),
    "Bhopal": ("Humid Subtropical", 25.0, 1146, "Oct–Feb", "Apr–Jun", "30–75%", "Lake city; moderate climate; good monsoon."),
    "Indore": ("Humid Subtropical", 24.5, 944, "Oct–Feb", "Apr–Jun", "30–70%", "Cleanest city; pleasant climate; moderate monsoon."),
    "Nagpur": ("Tropical Wet & Dry", 26.0, 1093, "Oct–Feb", "Apr–Jun", "30–75%", "Orange city; very hot summers; central India heat."),
    "Kochi": ("Tropical Monsoon", 27.0, 3005, "Dec–Feb", "Jun–Aug", "65–90%", "Heavy rainfall; backwater city; high humidity year-round."),
    "Thiruvananthapuram": ("Tropical Monsoon", 27.5, 1827, "Dec–Feb", "Jun–Aug", "70–90%", "Coastal; heavy monsoon; warm throughout."),
    "Visakhapatnam": ("Tropical Wet & Dry", 27.5, 1118, "Nov–Feb", "Apr–Jun", "55–85%", "Coastal; cyclone-prone; pleasant winters."),
    "Panaji": ("Tropical Monsoon", 27.0, 2932, "Nov–Feb", "Jun–Sep", "60–90%", "Goa capital; beach climate; heavy monsoon; tourist season Oct–Mar."),
    "Calangute": ("Tropical Monsoon", 27.0, 2932, "Nov–Feb", "Jun–Sep", "60–90%", "Coastal Goa; heavy monsoon; peak tourism Nov–Feb."),
    "Margao": ("Tropical Monsoon", 27.0, 2800, "Nov–Feb", "Jun–Sep", "60–90%", "South Goa hub; heavy monsoon; warm year-round."),
    "Vasco da Gama": ("Tropical Monsoon", 27.0, 2850, "Nov–Feb", "Jun–Sep", "60–90%", "Port city Goa; coastal; heavy monsoon."),
    "Mapusa": ("Tropical Monsoon", 27.0, 2900, "Nov–Feb", "Jun–Sep", "60–90%", "North Goa market town; heavy monsoon; warm climate."),
    "Coimbatore": ("Tropical Wet & Dry", 24.5, 700, "Nov–Feb", "Apr–May", "45–70%", "Manchester of South India; pleasant moderate climate."),
    "Vadodara": ("Hot Semi-arid", 27.0, 930, "Nov–Feb", "Apr–Jun", "30–75%", "Hot summers; moderate monsoon; cultural city."),
    "Surat": ("Tropical Wet & Dry", 27.5, 1143, "Nov–Feb", "Apr–Jun", "40–80%", "Diamond city; hot & humid; good monsoon."),
    "Patna": ("Humid Subtropical", 26.0, 1089, "Oct–Mar", "May–Jul", "40–85%", "Ganges plain; hot summers; flood-prone monsoon."),
    "Ranchi": ("Humid Subtropical", 23.0, 1430, "Oct–Feb", "May–Jul", "40–80%", "Plateau city; pleasant compared to plains; good monsoon."),
    "Dehradun": ("Humid Subtropical", 21.0, 2073, "Sep–Nov", "Jun–Aug", "45–85%", "Doon Valley; pleasant; heavy monsoon; cool winters."),
    "Shimla": ("Subtropical Highland", 13.0, 1577, "Mar–Jun", "Jul–Sep", "50–85%", "Hill station; snowfall in winter; pleasant summers."),
    "Guwahati": ("Humid Subtropical", 24.0, 1722, "Oct–Mar", "May–Jul", "60–90%", "Northeast gateway; heavy monsoon; warm & humid."),
    "Bhubaneswar": ("Tropical Savanna", 27.0, 1502, "Oct–Feb", "Apr–Jun", "50–85%", "Temple city; cyclone-prone; hot & humid summers."),
    "Mysuru": ("Tropical Savanna", 24.0, 798, "Sep–Feb", "Mar–May", "45–75%", "Heritage city; pleasant climate year-round."),
    "Amritsar": ("Humid Subtropical", 23.5, 680, "Oct–Mar", "May–Jul", "30–75%", "Hot summers; cold winters (near 0°C); moderate rainfall."),
    "Jodhpur": ("Hot Desert", 26.5, 360, "Oct–Mar", "May–Jul", "20–55%", "Blue city; Thar desert edge; extreme heat; very low rainfall."),
    "Udaipur": ("Hot Semi-arid", 25.0, 637, "Oct–Mar", "May–Jun", "25–65%", "Lake city; moderate Rajasthan climate; tourist hub."),
    "Varanasi": ("Humid Subtropical", 26.0, 1030, "Oct–Mar", "May–Jul", "35–80%", "Ganges city; very hot summers; monsoon flooding."),
    "Agra": ("Humid Subtropical", 25.5, 687, "Oct–Mar", "May–Jul", "30–75%", "Taj Mahal city; extreme summers; dry heat."),
    "Noida": ("Humid Subtropical", 25.0, 797, "Oct–Mar", "May–Jul", "30–80%", "NCR satellite; same as Delhi climate; AQI concerns."),
    "Greater Noida": ("Humid Subtropical", 25.0, 797, "Oct–Mar", "May–Jul", "30–80%", "NCR satellite; Delhi-like climate; newer developments."),
    "Gurugram": ("Humid Subtropical", 25.0, 797, "Oct–Mar", "May–Jul", "30–80%", "NCR tech hub; same as Delhi climate; AQI issues."),
    "Faridabad": ("Humid Subtropical", 25.0, 797, "Oct–Mar", "May–Jul", "30–80%", "NCR industrial; Delhi-like climate."),
    "Ghaziabad": ("Humid Subtropical", 25.0, 797, "Oct–Mar", "May–Jul", "30–80%", "NCR satellite; follows Delhi weather patterns."),
    "Thane": ("Tropical Wet", 27.0, 2500, "Nov–Feb", "Jun–Sep", "60–90%", "Mumbai satellite; heavy monsoon; lake city."),
    "Navi Mumbai": ("Tropical Wet", 27.0, 2300, "Nov–Feb", "Jun–Sep", "60–90%", "Planned city; similar to Mumbai; coastal."),
    "Nashik": ("Tropical Wet & Dry", 24.5, 890, "Oct–Feb", "Apr–Jun", "35–75%", "Wine capital; pleasant climate; moderate monsoon."),
    "Mangaluru": ("Tropical Monsoon", 27.0, 3799, "Nov–Feb", "Jun–Sep", "65–90%", "Coastal Karnataka; very heavy rainfall; warm year-round."),
    "Srinagar": ("Humid Subtropical", 13.5, 710, "Apr–Jun", "Dec–Feb", "45–75%", "Kashmir valley; cold winters with snowfall; pleasant summers."),
    "Kanpur": ("Humid Subtropical", 26.0, 840, "Oct–Mar", "May–Jul", "35–80%", "Industrial city; hot summers; Ganges plain climate."),
    "Madurai": ("Tropical Wet & Dry", 28.5, 850, "Nov–Feb", "Apr–Jun", "55–80%", "Temple city; hot & dry; moderate northeast monsoon."),
    "Vijayawada": ("Tropical Wet & Dry", 28.0, 1040, "Nov–Feb", "Apr–Jun", "55–85%", "Krishna river city; hot summers; cyclone-prone."),
    "Raipur": ("Tropical Wet & Dry", 26.5, 1300, "Oct–Feb", "Apr–Jun", "35–80%", "Chhattisgarh capital; hot summers; good monsoon."),
    "Rajkot": ("Hot Semi-arid", 26.5, 600, "Nov–Feb", "Apr–Jun", "25–65%", "Saurashtra region; hot & dry; limited monsoon."),
    "Jamshedpur": ("Humid Subtropical", 25.5, 1350, "Oct–Feb", "May–Jul", "40–80%", "Steel city; Chota Nagpur plateau; moderate climate."),
    "Mohali": ("Humid Subtropical", 23.5, 1050, "Oct–Mar", "May–Jul", "30–75%", "Tricity area; same as Chandigarh climate."),
    "Panchkula": ("Humid Subtropical", 23.5, 1050, "Oct–Mar", "May–Jul", "30–75%", "Tricity area; Shivalik foothills; pleasant."),
}

# ─── Sidebar ───
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Flag_of_India.svg/255px-Flag_of_India.svg.png", width=70)
    st.markdown("## 🇮🇳 Land Rate Analyzer")
    st.caption("All 28 States + 8 Union Territories")
    st.divider()

    # ── Location selectors (placed first so changes auto-navigate) ──
    st.markdown("#### 🔍 Select Location")
    all_states = get_all_states()
    selected_state = st.selectbox(
        "State / UT", all_states,
        index=all_states.index("Maharashtra") if "Maharashtra" in all_states else 0,
        label_visibility="collapsed",
        key="sel_state",
    )
    cities = get_cities_in_state(selected_state, df)
    selected_city = st.selectbox("City / Town", cities, label_visibility="collapsed", key="sel_city")
    selected_location = f"{selected_city}, {selected_state}"

    available_areas = get_areas_in_city(selected_city)
    selected_area = None
    if available_areas:
        area_options = ["🏙️ City Overview (All Areas)"] + available_areas
        area_choice = st.selectbox("Area / Locality", area_options, label_visibility="collapsed")
        if area_choice != "🏙️ City Overview (All Areas)":
            selected_area = area_choice
    else:
        st.caption("ℹ️ Area details not available for this city.")

    # Detect if user changed location → auto-navigate to Location Overview
    _prev_state = st.session_state.get("_prev_state", selected_state)
    _prev_city = st.session_state.get("_prev_city", selected_city)
    location_changed = (_prev_state != selected_state) or (_prev_city != selected_city)
    st.session_state["_prev_state"] = selected_state
    st.session_state["_prev_city"] = selected_city

    nav_default = 1 if location_changed else 0  # 1 = Location Overview

    st.divider()

    page = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Location Overview",
            "Rate Prediction",
            "Interactive Map",
            "Compare Locations",
            "Investment Calculator",
            "Legal Risk Checker",
            "Area Risk Alerts",
        ],
        icons=[
            "house-door-fill",
            "geo-alt-fill",
            "graph-up-arrow",
            "map-fill",
            "arrow-left-right",
            "calculator-fill",
            "shield-fill-check",
            "exclamation-triangle-fill",
        ],
        default_index=nav_default,
        key=f"nav_menu_{selected_state}_{selected_city}" if location_changed else "nav_menu",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#FF6B35", "font-size": "16px"},
            "nav-link": {
                "font-size": "14px", "text-align": "left", "margin": "2px 0",
                "padding": "8px 12px", "color": "#f0f0f0", "border-radius": "8px",
                "--hover-color": "rgba(255,107,53,0.12)",
            },
            "nav-link-selected": {
                "background-color": "rgba(255,107,53,0.12)",
                "color": "#FF6B35", "font-weight": "700",
            },
        },
    )

    # ─── Live Weather ───
    st.divider()
    weather = fetch_weather(selected_city)
    if weather:
        icon_url = weather["icon"]
        if icon_url.startswith("//"):
            icon_url = "https:" + icon_url
        st.markdown(f'''
        <div class="weather-card">
            <div style="font-size:0.72rem; color:#475569; margin-bottom:0.2rem; font-weight:600;">🌤 LIVE WEATHER</div>
            <div class="weather-top">
                <img src="{icon_url}" width="38" style="margin:-4px 0;">
                <span class="weather-temp">{weather["temp_c"]:.0f}°C</span>
            </div>
            <div class="weather-cond">{weather["condition"]}</div>
            <div class="weather-details">
                <div class="weather-detail-item"><div class="weather-detail-val">{weather["feels"]:.0f}°C</div>Feels like</div>
                <div class="weather-detail-item"><div class="weather-detail-val">{weather["humidity"]}%</div>Humidity</div>
                <div class="weather-detail-item"><div class="weather-detail-val">{weather["wind_kph"]:.0f} km/h</div>Wind</div>
            </div>
            <span class="aqi-badge" style="background:{weather['aqi_color']}20; color:{weather['aqi_color']};">AQI: {weather['aqi_label']}</span>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.caption("⛅ Weather data unavailable.")
    st.markdown("#### 📊 Quick Stats")
    st.metric("Locations", f"{df['Location'].nunique()}")
    st.metric("States & UTs", f"{df['State'].nunique()}")
    st.metric("Data Range", "2018 – 2026")


# ═══════════════════════════════════════════
#  🏠  HOME PAGE
# ═══════════════════════════════════════════
if page == "Home":

    latest_year = df["Year"].max()
    latest_df = df[df["Year"] == latest_year]
    avg_rate = latest_df["Rate_Per_SqFt"].mean()
    top_city = latest_df.loc[latest_df["Rate_Per_SqFt"].idxmax(), "Location"]
    top_rate = latest_df["Rate_Per_SqFt"].max()
    avg_growth = latest_df["Annual_Growth_Pct"].mean()
    total_locs = df["Location"].nunique()
    total_states = df["State"].nunique()

    # ── Hero Section ──
    st.markdown(f'''
    <div class="hero-wrap">
        <p class="main-header">India Land Rate Analyzer</p>
        <p class="sub-header">Intelligent land rate insights, predictions &amp; risk analysis across 200+ Indian cities</p>
        <span class="hero-badge">✦ Powered by Amonra Scarab &nbsp;·&nbsp; {total_locs} Locations &nbsp;·&nbsp; {total_states} States & UTs</span>
    </div>
    ''', unsafe_allow_html=True)

    # ── Key Numbers ──
    st.markdown(f'''
    <div class="stat-row">
        <div class="stat-pill"><div class="stat-val">{total_locs}</div><div class="stat-label">Cities & Towns</div></div>
        <div class="stat-pill"><div class="stat-val">₹{avg_rate:,.0f}</div><div class="stat-label">Avg Rate / sqft</div></div>
        <div class="stat-pill"><div class="stat-val">{top_city.split(",")[0]}</div><div class="stat-label">Highest Priced</div></div>
        <div class="stat-pill"><div class="stat-val">{avg_growth:.1f}%</div><div class="stat-label">Avg Annual Growth</div></div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    # ── Feature Cards ──
    def _feat(bg, icon, title, desc):
        return f'''<div class="feat-card">
            <div class="feat-icon" style="background:{bg};">{icon}</div>
            <div class="feat-title">{title}</div>
            <div class="feat-desc">{desc}</div>
        </div>'''

    def _step(bg, num, title, desc):
        return f'''<div class="step-card">
            <div style="display:flex; align-items:center;">
                <span class="step-num" style="background:{bg}; color:#fff;">{num}</span>
                <span class="step-title">{title}</span>
            </div>
            <p class="step-desc">{desc}</p>
        </div>'''

    st.markdown('<p class="section-hdr">Explore the Platform</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Eight powerful tools to help you research, analyze, and invest with confidence.</p>', unsafe_allow_html=True)

    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        st.markdown(_feat("linear-gradient(135deg,#FF6B35,#ff8c5a)", "◎", "Location Overview", "Current rates, growth trends, zone details &amp; development forecasts."), unsafe_allow_html=True)
    with fc2:
        st.markdown(_feat("linear-gradient(135deg,#00b894,#00d4aa)", "⬈", "Rate Prediction", "ML-powered 1–10 year forecasts with confidence intervals."), unsafe_allow_html=True)
    with fc3:
        st.markdown(_feat("linear-gradient(135deg,#6c5ce7,#a29bfe)", "◈", "Interactive Map", "Explore 200+ locations on an interactive color-coded India map."), unsafe_allow_html=True)
    with fc4:
        st.markdown(_feat("linear-gradient(135deg,#0984e3,#74b9ff)", "⇌", "Compare Cities", "Side-by-side comparison of up to 6 cities with radar charts."), unsafe_allow_html=True)

    st.markdown("")
    fc5, fc6, fc7, fc8 = st.columns(4)
    with fc5:
        st.markdown(_feat("linear-gradient(135deg,#fdcb6e,#e17055)", "◇", "Investment Calc", "Enter an amount &amp; horizon to project ROI and future profits."), unsafe_allow_html=True)
    with fc6:
        st.markdown(_feat("linear-gradient(135deg,#00cec9,#81ecec)", "⊘", "Legal Risk Check", "Stamp duty, RERA, CRZ, tribal law compliance &amp; due diligence."), unsafe_allow_html=True)
    with fc7:
        st.markdown(_feat("linear-gradient(135deg,#d63031,#ff7675)", "△", "Area Risk Alerts", "Flood, water scarcity, illegal layouts, disputes &amp; proximity risks."), unsafe_allow_html=True)
    with fc8:
        st.markdown(_feat("linear-gradient(135deg,#636e72,#b2bec3)", "⊞", "Locality Data", "30+ cities with neighbourhood rates, pin codes &amp; landmarks."), unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    # ── How It Works ──
    st.markdown('<p class="section-hdr">Getting Started</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Three simple steps to make data-driven land investment decisions.</p>', unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(_step("#FF6B35", "1", "Select Location", "Pick any State, City, or Locality from the sidebar to focus your analysis."), unsafe_allow_html=True)
    with s2:
        st.markdown(_step("#00b894", "2", "Explore Insights", "Navigate between pages — view rates, predictions, maps, legal checks &amp; more."), unsafe_allow_html=True)
    with s3:
        st.markdown(_step("#6c5ce7", "3", "Decide with Data", "Compare locations, run investment scenarios &amp; check legal risks before you invest."), unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    # ── Top Cities & Map side by side ──
    col_table, col_map = st.columns([1, 1], gap="large")

    with col_table:
        st.markdown('<p class="section-hdr">Top 10 Cities by Rate</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Highest land rates across India for the latest year.</p>', unsafe_allow_html=True)
        top10 = latest_df.nlargest(10, "Rate_Per_SqFt")[["Location", "Rate_Per_SqFt", "Annual_Growth_Pct", "Infrastructure_Score", "Zone_Type"]].copy()
        top10.columns = ["City", "Rate (₹/sqft)", "Growth %", "Infra Score", "Zone"]
        top10["Rate (₹/sqft)"] = top10["Rate (₹/sqft)"].apply(lambda v: f"₹{v:,.0f}")
        top10 = top10.reset_index(drop=True)
        top10.index = top10.index + 1
        st.dataframe(top10, use_container_width=True, height=420)

    with col_map:
        st.markdown('<p class="section-hdr">India at a Glance</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Land rates visualized across all covered locations.</p>', unsafe_allow_html=True)
        mini_map_df = latest_df.copy()
        mini_map_df["Rate_Display"] = mini_map_df["Rate_Per_SqFt"].apply(lambda v: f"₹{v:,.0f}/sqft")
        fig_mini = px.scatter_map(
            mini_map_df, lat="Latitude", lon="Longitude",
            color="Rate_Per_SqFt", size="Rate_Per_SqFt",
            hover_name="Location",
            hover_data={"Rate_Display": True, "Zone_Type": True, "Rate_Per_SqFt": False, "Latitude": False, "Longitude": False},
            color_continuous_scale="YlOrRd", size_max=18, zoom=3.6,
            center={"lat": 22.5, "lon": 82.0},
        )
        fig_mini.update_layout(map_style="carto-positron", height=420, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_mini, use_container_width=True)


# ═══════════════════════════════════════════
#  📍  LOCATION OVERVIEW
# ═══════════════════════════════════════════
elif page == "Location Overview":

    st.header(f"📍 {selected_location}")
    insights = get_location_insights(selected_location, df)

    if insights:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Current Rate", f"₹{insights['current_rate']:,.0f}/sqft")
        with col2:
            st.metric("📈 CAGR", f"{insights['cagr']}%")
        with col3:
            st.metric("🏗️ Infra Score", f"{insights['infrastructure_score']}/100")
        with col4:
            st.metric("🚀 Dev Potential", f"{insights['development_potential']}/100")

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("🏷️ Zone Type", insights["zone_type"])
            st.metric("🚌 Transport Score", f"{insights['transport_score']}/100")
        with col_b:
            st.metric("📊 Total Growth (2018-2026)", f"{insights['total_growth_pct']}%")
            st.metric("🏥 Amenities Score", f"{insights['amenities_score']}/100")

        # Historical Rate Chart
        loc_data = df[df["Location"] == selected_location].sort_values("Year")
        fig = px.line(
            loc_data, x="Year", y="Rate_Per_SqFt",
            title=f"📈 Historical Land Rate – {selected_location}",
            markers=True,
            labels={"Rate_Per_SqFt": "Rate (₹/sqft)", "Year": "Year"},
        )
        fig.update_traces(line=dict(color="#FF6B35", width=3), marker=dict(size=8))
        fig.update_layout(template="plotly_dark", height=420)
        st.plotly_chart(fig, use_container_width=True)

        # Area / Locality Details
        if selected_area:
            area_detail = get_area_details(selected_city, selected_area, insights["current_rate"])
            if area_detail:
                st.divider()
                st.subheader(f"📌 Area Spotlight – {selected_area}")
                ar1, ar2, ar3, ar4 = st.columns(4)
                with ar1:
                    st.metric("💰 Est. Rate", f"₹{area_detail['estimated_rate']:,}/sqft")
                with ar2:
                    prem_delta = f"{'+' if area_detail['premium_pct'] >= 0 else ''}{area_detail['premium_pct']}%"
                    st.metric("📊 vs City Avg", prem_delta)
                with ar3:
                    st.metric("🔗 Connectivity", f"{area_detail['connectivity_score']}/100")
                with ar4:
                    st.metric("📍 Distance", f"{area_detail['distance_from_center_km']} km")

                ar_a, ar_b = st.columns(2)
                with ar_a:
                    st.markdown(f"**🏷️ Area Type:** {area_detail['type']}")
                    st.markdown(f"**📮 Pin Code:** {area_detail['pin_code']}")
                    metro_text = "✅ Yes" if area_detail["metro_nearby"] else "❌ No"
                    st.markdown(f"**🚇 Metro Nearby:** {metro_text}")
                with ar_b:
                    st.markdown(f"**👥 Popular For:** {area_detail['popular_for']}")
                    st.markdown(f"**🏗️ Upcoming:** {area_detail['upcoming_development']}")
                    lm = ", ".join(area_detail["landmarks"])
                    st.markdown(f"**🗺️ Landmarks:** {lm}")

        # All Areas Comparison
        if not selected_area and available_areas:
            all_areas = get_all_area_details(selected_city, insights["current_rate"])
            if all_areas:
                st.divider()
                st.subheader(f"🏘️ Localities in {selected_city} – Rate Comparison")

                area_names = [a["area_name"] for a in all_areas]
                area_rates = [a["estimated_rate"] for a in all_areas]
                area_types = [a["type"] for a in all_areas]
                bar_colors = ["#FF6B35" if a["rate_multiplier"] >= 1.2 else "#00D4AA" if a["rate_multiplier"] <= 0.85 else "#4ECDC4" for a in all_areas]

                fig_areas = go.Figure(go.Bar(
                    x=area_names, y=area_rates,
                    marker_color=bar_colors,
                    text=[f"₹{r:,}" for r in area_rates],
                    textposition="outside",
                    hovertext=[f"{n}<br>Type: {t}<br>Rate: ₹{r:,}/sqft" for n, t, r in zip(area_names, area_types, area_rates)],
                    hoverinfo="text",
                ))
                fig_areas.add_hline(y=insights["current_rate"], line_dash="dash", line_color="white",
                                    annotation_text=f"City Avg: ₹{insights['current_rate']:,.0f}", annotation_position="top right")
                fig_areas.update_layout(
                    title=f"Estimated Rates by Locality – {selected_city}",
                    yaxis_title="Rate (₹/sqft)", xaxis_title="Locality",
                    template="plotly_dark", height=420, xaxis_tickangle=-45, margin=dict(b=120),
                )
                st.plotly_chart(fig_areas, use_container_width=True)

                area_table = []
                for a in all_areas:
                    metro_icon = "✅" if a["metro_nearby"] else "❌"
                    area_table.append({
                        "Locality": a["area_name"],
                        "Est. Rate (₹/sqft)": f"₹{a['estimated_rate']:,}",
                        "vs City Avg": f"{'+' if a['premium_pct'] >= 0 else ''}{a['premium_pct']}%",
                        "Type": a["type"],
                        "Connectivity": f"{a['connectivity_score']}/100",
                        "Metro": metro_icon,
                        "Distance (km)": a["distance_from_center_km"],
                        "Popular For": a["popular_for"],
                    })
                st.dataframe(pd.DataFrame(area_table), use_container_width=True, hide_index=True)
                st.caption("🟠 Premium area (20%+ above avg) | 🟢 Budget area (15%+ below avg) | 🔵 Mid-segment")

        # Development Forecast
        forecast = get_development_forecast(df, selected_location, dev_factors)
        if forecast:
            st.divider()
            st.subheader("🏗️ Development Forecast")
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                st.metric("Outlook", forecast["outlook"])
                st.metric("Risk Level", forecast["risk_level"])
            with fc2:
                st.metric("Overall Score", f"{forecast['overall_score']}/100")
                st.metric("Growth Multiplier", f"{forecast['growth_multiplier']}x")
            with fc3:
                st.info(f"**Key Drivers:** {', '.join(forecast['key_drivers'])}")
                st.info(f"**Forecast:** {forecast['forecast']}")

        # ── Climate Summary ──
        climate = CITY_CLIMATE.get(selected_city)
        if climate:
            c_type, c_avg_temp, c_rain, c_best, c_worst, c_humidity, c_note = climate
            st.divider()
            st.subheader("🌦️ Climate & Environment")

            clim_html = f'''
            <div class="climate-card">
                <div class="climate-grid">
                    <div><div class="climate-item-label">🌡️ Climate Type</div><div class="climate-item-val">{c_type}</div></div>
                    <div><div class="climate-item-label">🌡️ Avg Temperature</div><div class="climate-item-val">{c_avg_temp}°C</div></div>
                    <div><div class="climate-item-label">🌧️ Avg Annual Rainfall</div><div class="climate-item-val">{c_rain:,} mm</div></div>
                    <div><div class="climate-item-label">💧 Humidity Range</div><div class="climate-item-val">{c_humidity}</div></div>
                    <div><div class="climate-item-label">☀️ Best Months</div><div class="climate-item-val">{c_best}</div></div>
                    <div><div class="climate-item-label">⛈️ Tough Months</div><div class="climate-item-val">{c_worst}</div></div>
                </div>
                <div class="climate-note">📝 {c_note}</div>
            </div>
            '''
            st.markdown(clim_html, unsafe_allow_html=True)

            # Show live AQI detail if available
            w = fetch_weather(selected_city)
            if w and w.get("aqi_epa"):
                aqi_cols = st.columns(3)
                with aqi_cols[0]:
                    st.metric("🌫️ Air Quality", w["aqi_label"])
                with aqi_cols[1]:
                    st.metric("PM2.5", f"{w['pm25']:.1f} µg/m³" if w["pm25"] else "N/A")
                with aqi_cols[2]:
                    st.metric("PM10", f"{w['pm10']:.1f} µg/m³" if w["pm10"] else "N/A")
    else:
        st.warning("No data available for this location.")


# ═══════════════════════════════════════════
#  📈  RATE PREDICTION
# ═══════════════════════════════════════════
elif page == "Rate Prediction":

    st.header(f"📈 Rate Prediction – {selected_location}")
    st.caption("ML-powered price forecasting using polynomial regression with confidence intervals.")
    st.markdown("")

    years_ahead = st.slider("Prediction Horizon (Years)", 1, 10, 5, key="pred_years")

    prediction = predict_future_rates(df, selected_location, years_ahead)
    if prediction:
        st.success(f"Model Accuracy (R²): **{prediction['model_r2']:.4f}** | Current Rate: **₹{prediction['current_rate']:,.0f}/sqft**")

        hist = prediction["historical"]
        pred_df = prediction["predictions"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["Year"], y=hist["Rate_Per_SqFt"],
            mode="lines+markers", name="Historical",
            line=dict(color="#FF6B35", width=3), marker=dict(size=8),
        ))
        fig.add_trace(go.Scatter(
            x=pred_df["Year"], y=pred_df["Predicted_Rate"],
            mode="lines+markers", name="Predicted",
            line=dict(color="#00D4AA", width=3, dash="dash"), marker=dict(size=8, symbol="diamond"),
        ))
        fig.add_trace(go.Scatter(
            x=pd.concat([pred_df["Year"], pred_df["Year"][::-1]]),
            y=pd.concat([pred_df["Upper_Bound"], pred_df["Lower_Bound"][::-1]]),
            fill="toself", fillcolor="rgba(0,212,170,0.15)",
            line=dict(color="rgba(0,0,0,0)"), name="95% Confidence",
        ))
        fig.update_layout(
            title=f"Rate Forecast – {selected_location}",
            xaxis_title="Year", yaxis_title="Rate (₹/sqft)",
            template="plotly_dark", height=480,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Prediction Table")
        display_pred = pred_df.copy()
        for c in ["Predicted_Rate", "Lower_Bound", "Upper_Bound"]:
            display_pred[c] = display_pred[c].apply(lambda v: f"₹{v:,.0f}")
        display_pred["Confidence"] = display_pred["Confidence"].apply(lambda v: f"{v:.0%}")
        st.dataframe(display_pred, use_container_width=True)
    else:
        st.warning("Insufficient data for prediction.")


# ═══════════════════════════════════════════
#  🗺️  INTERACTIVE MAP
# ═══════════════════════════════════════════
elif page == "Interactive Map":

    st.header("🗺️ India Land Rate Map")
    st.caption("Explore land rates across all 200+ locations in India for any year.")
    st.markdown("")

    mcol1, mcol2 = st.columns([3, 1])
    with mcol1:
        map_year = st.select_slider("Select Year", options=sorted(df["Year"].unique()), value=df["Year"].max(), key="map_year")
    with mcol2:
        color_by = st.selectbox("Color By", ["Rate_Per_SqFt", "Infrastructure_Score", "Development_Potential", "Annual_Growth_Pct"], key="map_color")

    map_df = df[df["Year"] == map_year].copy()
    map_df["Rate_Display"] = map_df["Rate_Per_SqFt"].apply(lambda v: f"₹{v:,.0f}/sqft")

    color_labels = {
        "Rate_Per_SqFt": "Rate (₹/sqft)",
        "Infrastructure_Score": "Infra Score",
        "Development_Potential": "Dev Potential",
        "Annual_Growth_Pct": "Growth %",
    }

    fig_map = px.scatter_map(
        map_df, lat="Latitude", lon="Longitude",
        color=color_by, size="Rate_Per_SqFt",
        hover_name="Location",
        hover_data={"Rate_Display": True, "Zone_Type": True, "Infrastructure_Score": True,
                    "Rate_Per_SqFt": False, "Latitude": False, "Longitude": False},
        color_continuous_scale="YlOrRd",
        size_max=25, zoom=4,
        center={"lat": 22.5, "lon": 82.0},
        title=f"India Land Rates – {map_year}",
        labels={color_by: color_labels.get(color_by, color_by)},
    )
    fig_map.update_layout(map_style="carto-positron", height=650, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    with st.expander(f"📊 State-wise Summary ({map_year})", expanded=False):
        state_summary = map_df.groupby("State").agg(
            Avg_Rate=("Rate_Per_SqFt", "mean"),
            Max_Rate=("Rate_Per_SqFt", "max"),
            Min_Rate=("Rate_Per_SqFt", "min"),
            Locations=("Location", "count"),
            Avg_Infra=("Infrastructure_Score", "mean"),
        ).round(0).sort_values("Avg_Rate", ascending=False)
        state_summary["Avg_Rate"] = state_summary["Avg_Rate"].apply(lambda v: f"₹{v:,.0f}")
        state_summary["Max_Rate"] = state_summary["Max_Rate"].apply(lambda v: f"₹{v:,.0f}")
        state_summary["Min_Rate"] = state_summary["Min_Rate"].apply(lambda v: f"₹{v:,.0f}")
        st.dataframe(state_summary, use_container_width=True)


# ═══════════════════════════════════════════
#  ⚖️  COMPARE LOCATIONS
# ═══════════════════════════════════════════
elif page == "Compare Locations":

    st.header("⚖️ Compare Locations")
    st.caption("Select 2–6 cities for a side-by-side comparison on rates, growth, and infrastructure.")
    st.markdown("")

    all_locations = sorted(df["Location"].unique())
    compare_locs = st.multiselect(
        "Select locations to compare (2–6)",
        all_locations,
        default=[selected_location],
        max_selections=6,
        key="compare_select",
    )

    if len(compare_locs) >= 2:
        comp_df = compare_locations(df, compare_locs, dev_factors)
        if not comp_df.empty:
            st.dataframe(comp_df, use_container_width=True)

            comp_data = df[df["Location"].isin(compare_locs)]
            fig_comp = px.line(
                comp_data, x="Year", y="Rate_Per_SqFt", color="Location",
                title="Rate Comparison Over Time",
                markers=True,
                labels={"Rate_Per_SqFt": "Rate (₹/sqft)"},
            )
            fig_comp.update_layout(template="plotly_dark", height=450)
            st.plotly_chart(fig_comp, use_container_width=True)

            radar_metrics = ["Infra_Score", "Dev_Potential", "CAGR_%", "Growth_Multiplier"]
            available_metrics = [m for m in radar_metrics if m in comp_df.columns]
            if len(available_metrics) >= 3:
                fig_radar = go.Figure()
                for _, row in comp_df.iterrows():
                    values = [row[m] if pd.notna(row[m]) else 0 for m in available_metrics]
                    max_vals = [comp_df[m].max() if comp_df[m].max() > 0 else 1 for m in available_metrics]
                    norm_vals = [v / mx * 100 for v, mx in zip(values, max_vals)]
                    norm_vals.append(norm_vals[0])
                    labels = available_metrics + [available_metrics[0]]
                    fig_radar.add_trace(go.Scatterpolar(
                        r=norm_vals, theta=labels, fill="toself", name=row["Location"][:30],
                    ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 110])),
                    title="Location Comparison Radar", template="plotly_dark", height=450,
                )
                st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("👆 Select at least **2 locations** above to compare.")


# ═══════════════════════════════════════════
#  💰  INVESTMENT CALCULATOR
# ═══════════════════════════════════════════
elif page == "Investment Calculator":

    st.header("💰 Investment Calculator")
    st.caption(f"Estimate your return on investment for land in **{selected_location}**.")
    st.markdown("")

    inv_col1, inv_col2 = st.columns(2)
    with inv_col1:
        investment = st.number_input(
            "Investment Amount (₹)", min_value=100000, max_value=1000000000,
            value=5000000, step=500000, format="%d", key="inv_amount",
        )
    with inv_col2:
        inv_years = st.slider("Investment Horizon (Years)", 1, 10, 5, key="inv_years")

    st.markdown("")

    if st.button("🔮 Calculate ROI", type="primary", key="calc_roi"):
        roi = calculate_investment_roi(df, selected_location, investment, inv_years)
        if roi:
            st.success(f"**{selected_location}** | Investment: ₹{investment:,.0f} | Area: {roi['area_sqft']:,.1f} sqft | Current Rate: ₹{roi['current_rate']:,.0f}/sqft")

            projections = roi["projections"]
            if not projections.empty:
                last = projections.iloc[-1]
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric(f"Projected Value ({int(last['Year'])})", f"₹{last['Projected_Value_₹']:,.0f}")
                with m2:
                    st.metric("Total Profit", f"₹{last['Profit_₹']:,.0f}")
                with m3:
                    st.metric("ROI", f"{last['ROI_Pct']:.1f}%")

                fig_roi = go.Figure()
                fig_roi.add_trace(go.Bar(
                    x=projections["Year"].astype(str), y=projections["Projected_Value_₹"],
                    name="Projected Value", marker_color="#FF6B35",
                ))
                fig_roi.add_hline(y=investment, line_dash="dash", line_color="white", annotation_text="Investment")
                fig_roi.update_layout(
                    title=f"Investment Growth – {selected_location}",
                    xaxis_title="Year", yaxis_title="Value (₹)",
                    template="plotly_dark", height=420,
                )
                st.plotly_chart(fig_roi, use_container_width=True)

                st.subheader("📋 Year-wise Projection")
                display_proj = projections.copy()
                display_proj["Projected_Value_₹"] = display_proj["Projected_Value_₹"].apply(lambda v: f"₹{v:,.0f}")
                display_proj["Profit_₹"] = display_proj["Profit_₹"].apply(lambda v: f"₹{v:,.0f}")
                display_proj["Rate_Per_SqFt"] = display_proj["Rate_Per_SqFt"].apply(lambda v: f"₹{v:,.0f}")
                st.dataframe(display_proj, use_container_width=True)
        else:
            st.error("Could not calculate ROI. Insufficient data.")


# ═══════════════════════════════════════════
#  🛡️  LEGAL RISK CHECKER
# ═══════════════════════════════════════════
elif page == "Legal Risk Checker":

    st.header(f"🛡️ Legal Risk Checker – {selected_location}")
    st.caption("Comprehensive legal due diligence assessment based on state-specific land laws and zone type.")
    st.markdown("")

    insights_legal = get_location_insights(selected_location, df)
    zone = insights_legal["zone_type"] if insights_legal else "Tier-2 City"
    legal = get_legal_risk_profile(selected_state, zone, location=selected_location)

    # Risk Score Header
    rs_col1, rs_col2, rs_col3, rs_col4 = st.columns(4)
    with rs_col1:
        st.metric("⚖️ Risk Score", f"{legal['risk_score']}/100")
    with rs_col2:
        st.metric("Risk Level", legal["risk_level"])
    with rs_col3:
        st.metric("Stamp Duty + Registration", f"{legal['total_duty_pct']}%")
    with rs_col4:
        st.metric("Agri → NA Conversion", legal["state_law"]["agri_conversion_ease"])

    # Risk Gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=legal["risk_score"],
        title={"text": f"Legal Risk Score – {selected_state}", "font": {"size": 18}},
        delta={"reference": 50, "increasing": {"color": "red"}, "decreasing": {"color": "green"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": "#FF6B35"},
            "steps": [
                {"range": [0, 35], "color": "#2d6a4f"},
                {"range": [35, 50], "color": "#f4a261"},
                {"range": [50, 70], "color": "#e76f51"},
                {"range": [70, 100], "color": "#d62828"},
            ],
            "threshold": {"line": {"color": "white", "width": 3}, "thickness": 0.8, "value": legal["risk_score"]},
        },
    ))
    fig_gauge.update_layout(template="plotly_dark", height=300, margin=dict(t=60, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Warnings
    if legal["warnings"]:
        with st.expander("⚠️ State-Specific Warnings", expanded=True):
            for w in legal["warnings"]:
                st.warning(w)

    # Land Law Summary
    with st.expander(f"📜 {selected_state} – Land Law Summary", expanded=False):
        sl = legal["state_law"]
        law_col1, law_col2 = st.columns(2)
        with law_col1:
            rera_txt = "✅ Yes" if sl["rera_active"] else "❌ No"
            ceiling_txt = "✅ Yes" if sl["land_ceiling_act"] else "❌ No"
            nri_txt = "✅ Yes" if sl["nri_allowed"] else "🚫 No / Restricted"
            tribal_txt = "⚠️ Yes" if sl["tribal_restriction"] else "✅ None"
            st.markdown(f"- **RERA Active:** {rera_txt}")
            st.markdown(f"- **Land Ceiling Act:** {ceiling_txt}")
            st.markdown(f"- **NRI / Outsiders Can Buy:** {nri_txt}")
            st.markdown(f"- **Tribal Land Restrictions:** {tribal_txt}")
        with law_col2:
            crz_txt = "🌊 Applicable" if sl["coastal_zone"] else "➖ Not Applicable"
            st.markdown(f"- **Coastal Zone (CRZ):** {crz_txt}")
            st.markdown(f"- **Stamp Duty:** {sl['stamp_duty_pct']}%")
            st.markdown(f"- **Registration Fee:** {sl['registration_pct']}%")
            st.markdown(f"- **Agri → NA Conversion:** {sl['agri_conversion_ease']}")
        st.info(f"📌 **Special Notes:** {sl['special_notes']}")

    # Legal Risk Checklist
    with st.expander("🔍 Legal Risk Checklist (by Category)", expanded=False):
        for cat in legal["common_risks"]:
            st.markdown(f"**📂 {cat['category']}**")
            for risk in cat["risks"]:
                severity_badge = {
                    "Critical": "🔴 CRITICAL", "High": "🟠 HIGH", "Medium": "🟡 MEDIUM", "Low": "🟢 LOW",
                }.get(risk["severity"], risk["severity"])
                st.markdown(f"- **{risk['icon']} {risk['name']}** — {severity_badge}  \n  {risk['description']}")
            st.markdown("---")

    # Cost Estimator
    with st.expander("💸 Registration Cost Estimator", expanded=True):
        sl = legal["state_law"]
        property_value = st.number_input(
            "Estimated Property Value (₹)", min_value=100000, max_value=1000000000,
            value=5000000, step=500000, format="%d", key="legal_prop_val",
        )

        stamp_duty_amt = property_value * sl["stamp_duty_pct"] / 100
        reg_amt = property_value * sl["registration_pct"] / 100
        tds_amt = property_value * 0.01 if property_value > 5000000 else 0
        gst_amt = property_value * 0.05
        total_cost = stamp_duty_amt + reg_amt

        cost_col1, cost_col2, cost_col3, cost_col4 = st.columns(4)
        with cost_col1:
            st.metric("Stamp Duty", f"₹{stamp_duty_amt:,.0f}")
        with cost_col2:
            st.metric("Registration Fee", f"₹{reg_amt:,.0f}")
        with cost_col3:
            st.metric("TDS (if > ₹50L)", f"₹{tds_amt:,.0f}")
        with cost_col4:
            st.metric("Total Duty + Reg", f"₹{total_cost:,.0f}")

        st.caption(f"💡 GST (if under-construction, non-affordable): ₹{gst_amt:,.0f} @ 5% — not included in total above.")

        if total_cost > 0:
            fig_pie = go.Figure(go.Pie(
                labels=["Stamp Duty", "Registration Fee", "TDS (if applicable)"],
                values=[stamp_duty_amt, reg_amt, tds_amt],
                hole=0.45,
                marker_colors=["#FF6B35", "#00D4AA", "#F4A261"],
                textinfo="label+percent+value",
                texttemplate="%{label}<br>₹%{value:,.0f}<br>(%{percent})",
            ))
            fig_pie.update_layout(title="Registration Cost Breakdown", template="plotly_dark", height=380)
            st.plotly_chart(fig_pie, use_container_width=True)

    # Recommendations
    with st.expander("✅ Recommendations & Best Practices", expanded=False):
        for rec in legal["recommendations"]:
            st.markdown(rec)

    # Document Checklist
    with st.expander("📋 Document Checklist", expanded=False):
        doc_col1, doc_col2 = st.columns(2)
        mid = len(legal["documents"]) // 2
        with doc_col1:
            for doc in legal["documents"][:mid]:
                st.checkbox(doc, key=f"doc_{doc}")
        with doc_col2:
            for doc in legal["documents"][mid:]:
                st.checkbox(doc, key=f"doc_{doc}")

    st.markdown("")
    st.error("⚠️ **Disclaimer:** This is an educational tool. Always consult a qualified property lawyer and conduct independent due diligence before any land transaction in India.")


# ═══════════════════════════════════════════
#  🚨  AREA RISK ALERTS
# ═══════════════════════════════════════════
elif page == "Area Risk Alerts":

    st.header(f"🚨 Area Risk Alerts – {selected_location}")
    st.caption("Environmental, safety, and development proximity risk assessment for your selected location.")
    st.markdown("")

    insights_area = get_location_insights(selected_location, df)
    if insights_area:
        zone_area = insights_area["zone_type"]
        infra_area = insights_area["infrastructure_score"]
        loc_data_area = df[df["Location"] == selected_location].iloc[-1]
        lat_area = loc_data_area["Latitude"]
        lon_area = loc_data_area["Longitude"]

        area_risks = get_area_risk_alerts(selected_location, selected_state, zone_area, infra_area, lat_area, lon_area)

        # Overall Score
        ov_col1, ov_col2, ov_col3 = st.columns([1, 2, 1])
        with ov_col1:
            st.metric("Overall Area Risk", f"{area_risks['overall_score']}/100")
        with ov_col2:
            st.metric("Risk Rating", area_risks["overall_label"])
        with ov_col3:
            st.metric("Zone Type", zone_area)

        # Charts side by side
        scores = area_risks["risk_scores"]
        radar_labels = ["🌊 Flood", "🏜️ Water Scarcity", "🚨 Illegal Layouts", "⚖️ Land Disputes", "📍 Dev. Distance"]
        radar_keys = ["flood", "water_scarcity", "illegal_layout", "land_dispute", "dev_distance"]
        radar_values = [scores[k] for k in radar_keys]
        radar_values_closed = radar_values + [radar_values[0]]
        radar_labels_closed = radar_labels + [radar_labels[0]]

        chart_left, chart_right = st.columns(2)

        with chart_left:
            fig_radar_area = go.Figure()
            fig_radar_area.add_trace(go.Scatterpolar(
                r=radar_values_closed, theta=radar_labels_closed,
                fill="toself", fillcolor="rgba(255, 107, 53, 0.25)",
                line=dict(color="#FF6B35", width=2),
                name=selected_city,
            ))
            fig_radar_area.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
                    angularaxis=dict(tickfont=dict(size=11)),
                ),
                title=f"Risk Radar – {selected_city}",
                template="plotly_dark", height=420,
                margin=dict(t=60, b=30, l=60, r=60),
            )
            st.plotly_chart(fig_radar_area, use_container_width=True)

        with chart_right:
            bar_colors = []
            for v in radar_values:
                if v >= 70:
                    bar_colors.append("#d62828")
                elif v >= 45:
                    bar_colors.append("#f4a261")
                elif v >= 30:
                    bar_colors.append("#e9c46a")
                else:
                    bar_colors.append("#2d6a4f")

            fig_bar_risk = go.Figure(go.Bar(
                x=radar_labels, y=radar_values,
                marker_color=bar_colors,
                text=[f"{v}/100" for v in radar_values],
                textposition="outside",
            ))
            fig_bar_risk.add_hline(y=70, line_dash="dash", line_color="#d62828", annotation_text="High Risk", annotation_position="top right")
            fig_bar_risk.add_hline(y=45, line_dash="dash", line_color="#f4a261", annotation_text="Moderate", annotation_position="top right")
            fig_bar_risk.update_layout(
                title="Risk Scores by Category",
                yaxis_title="Risk Score (0–100)", yaxis_range=[0, 110],
                template="plotly_dark", height=420,
            )
            st.plotly_chart(fig_bar_risk, use_container_width=True)

        # Detailed Alert Cards
        st.subheader("📋 Detailed Risk Alerts")
        for alert in area_risks["alerts"]:
            severity_colors = {"High": "🔴", "Moderate": "🟠", "Low-Moderate": "🟡", "Low": "🟢"}
            sev_icon = severity_colors.get(alert["severity"], "⚪")
            with st.expander(f"{alert['icon']} {alert['title']}  |  {sev_icon} {alert['severity']}", expanded=(alert["severity"] in ["High", "Moderate"])):
                st.markdown(f"**{alert['detail']}**")
                st.markdown("---")
                st.markdown(f"💡 **Recommendation:** {alert['recommendation']}")

        # Risk Summary Table
        with st.expander("📊 Risk Summary Table", expanded=False):
            summary_data = []
            risk_display = {
                "flood": ("🌊 Flood Risk", "Flooding, waterlogging, drainage"),
                "water_scarcity": ("🏜️ Water Scarcity", "Groundwater, municipal supply"),
                "illegal_layout": ("🚨 Illegal Layouts", "Unauthorized colonies, unapproved plots"),
                "land_dispute": ("⚖️ Land Disputes", "Title disputes, acquisition, litigation"),
                "dev_distance": ("📍 Dev. Distance", "Proximity to IT/industrial/commercial hubs"),
            }
            for key, (label, desc) in risk_display.items():
                score = scores[key]
                if score >= 70:
                    level = "🔴 High"
                elif score >= 45:
                    level = "🟠 Moderate"
                elif score >= 30:
                    level = "🟡 Low-Moderate"
                else:
                    level = "🟢 Low"
                summary_data.append({"Risk Category": label, "Score": f"{score}/100", "Level": level, "About": desc})
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

        # Mitigation Checklist
        with st.expander("✅ Area Risk Mitigation Checklist", expanded=False):
            checklist_items = [
                "Check NDMA / state disaster management flood zone maps",
                "Verify CGWB groundwater level data for the locality",
                "Confirm municipal water supply connection & hours",
                "Verify layout approval from Development Authority (DTCP/DA/HMDA/BDA etc.)",
                "Search local court records for pending land disputes",
                "Check city master plan for zone classification & future projects",
                "Verify proximity to metro/railway/highway in master plan",
                "Inspect local drainage and sewage infrastructure",
                "Check for nearby eco-sensitive / CRZ / forest buffer zones",
                "Talk to local residents about historical issues (flooding, disputes, scams)",
            ]
            chk_col1, chk_col2 = st.columns(2)
            mid_chk = len(checklist_items) // 2
            with chk_col1:
                for item in checklist_items[:mid_chk]:
                    st.checkbox(item, key=f"area_chk_{item[:20]}")
            with chk_col2:
                for item in checklist_items[mid_chk:]:
                    st.checkbox(item, key=f"area_chk_{item[:20]}")

        st.markdown("")
        st.error("⚠️ **Disclaimer:** Area risk data is based on historical patterns, state-level statistics, and publicly available reports. Always conduct on-ground verification and consult local experts.")
    else:
        st.warning("No data available for this location.")


# ─── Footer ───
st.divider()
st.markdown("""
<div style='text-align:center; color:#666; font-size:0.82rem; padding: 0.5rem 0;'>
    🇮🇳 India Land Rate Analyzer  ·  200+ locations across 28 States & 8 Union Territories<br>
    ⚠️ Data is simulated for educational purposes. Consult local experts for actual investment decisions.<br>
    Built with ❤️ using Streamlit · Plotly · scikit-learn
</div>
""", unsafe_allow_html=True)

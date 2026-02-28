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
    .block-container { padding-top: 1.5rem; }
    .main-header {
        font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(90deg, #FF6B35 0%, #F7C948 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0.2rem;
    }
    .sub-header { font-size: 1rem; color: #aaa; text-align: center; margin-bottom: 1.6rem; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1117 0%, #161b22 100%); }
    .feature-card {
        background: rgba(255,255,255,0.04); padding: 1.4rem; border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08); text-align: center;
    }
    .feature-icon  { font-size: 2.4rem; margin-bottom: 0.6rem; }
    .feature-title { font-size: 1.05rem; font-weight: 600; margin-bottom: 0.3rem; color: #FF6B35; }
    .feature-desc  { font-size: 0.85rem; color: #aaa; }
    .step-num {
        display: inline-block; width: 32px; height: 32px; background: #FF6B35; color: #fff;
        border-radius: 50%; text-align: center; line-height: 32px; font-weight: 700; margin-right: 0.6rem;
    }
    .stMetric { background: rgba(255,107,53,0.06); border-radius: 10px; padding: 0.8rem; }
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

# ─── Sidebar ───
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Flag_of_India.svg/255px-Flag_of_India.svg.png", width=70)
    st.markdown("## 🇮🇳 Land Rate Analyzer")
    st.caption("All 28 States + 8 Union Territories")
    st.divider()

    page = st.radio(
        "Navigate",
        [
            "🏠 Home",
            "📍 Location Overview",
            "📈 Rate Prediction",
            "🗺️ Interactive Map",
            "⚖️ Compare Locations",
            "💰 Investment Calculator",
            "🛡️ Legal Risk Checker",
            "🚨 Area Risk Alerts",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("#### 🔍 Select Location")
    all_states = get_all_states()
    selected_state = st.selectbox(
        "State / UT", all_states,
        index=all_states.index("Maharashtra") if "Maharashtra" in all_states else 0,
        label_visibility="collapsed",
    )
    cities = get_cities_in_state(selected_state, df)
    selected_city = st.selectbox("City / Town", cities, label_visibility="collapsed")
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

    st.divider()
    st.markdown("#### 📊 Quick Stats")
    st.metric("Locations", f"{df['Location'].nunique()}")
    st.metric("States & UTs", f"{df['State'].nunique()}")
    st.metric("Data Range", "2018 – 2026")


# ═══════════════════════════════════════════
#  🏠  HOME PAGE
# ═══════════════════════════════════════════
if page == "🏠 Home":

    st.markdown('<p class="main-header">🇮🇳 India Land Rate Analyzer & Predictor</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your one-stop platform for land rate insights across 200+ Indian cities & towns</p>', unsafe_allow_html=True)

    latest_year = df["Year"].max()
    latest_df = df[df["Year"] == latest_year]
    avg_rate = latest_df["Rate_Per_SqFt"].mean()
    top_city = latest_df.loc[latest_df["Rate_Per_SqFt"].idxmax(), "Location"]
    top_rate = latest_df["Rate_Per_SqFt"].max()
    avg_growth = latest_df["Annual_Growth_Pct"].mean()

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🏙️ Cities Covered", f"{df['Location'].nunique()}")
    with m2:
        st.metric("📊 Avg Rate (2026)", f"₹{avg_rate:,.0f}/sqft")
    with m3:
        st.metric("🏆 Highest Rate City", top_city.split(",")[0], f"₹{top_rate:,.0f}/sqft")
    with m4:
        st.metric("📈 Avg Growth", f"{avg_growth:.1f}%")

    st.markdown("")

    # Feature Cards
    st.markdown("### ✨ What You Can Do")
    st.markdown("")

    def _feature_card(icon, title, desc):
        return f'<div class="feature-card"><div class="feature-icon">{icon}</div><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>'

    def _step_card(num, title, desc):
        return f'<div class="feature-card" style="text-align:left; padding:1.6rem;"><span class="step-num">{num}</span><strong>{title}</strong><p style="margin-top:0.6rem; color:#bbb; font-size:0.9rem;">{desc}</p></div>'

    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        st.markdown(_feature_card("📍", "Location Overview", "View current rates, growth trends, area-level details &amp; development forecasts."), unsafe_allow_html=True)
    with fc2:
        st.markdown(_feature_card("📈", "Rate Prediction", "ML-powered 1–10 year price predictions with confidence intervals."), unsafe_allow_html=True)
    with fc3:
        st.markdown(_feature_card("🗺️", "Interactive Map", "Explore all 200+ locations on a color-coded map of India."), unsafe_allow_html=True)
    with fc4:
        st.markdown(_feature_card("⚖️", "Compare Locations", "Side-by-side comparison of up to 6 cities with radar charts."), unsafe_allow_html=True)

    st.markdown("")
    fc5, fc6, fc7, fc8 = st.columns(4)
    with fc5:
        st.markdown(_feature_card("💰", "Investment Calculator", "Enter an amount &amp; horizon to see projected ROI and profits."), unsafe_allow_html=True)
    with fc6:
        st.markdown(_feature_card("🛡️", "Legal Risk Checker", "Due diligence on stamp duty, RERA, CRZ, tribal laws &amp; more."), unsafe_allow_html=True)
    with fc7:
        st.markdown(_feature_card("🚨", "Area Risk Alerts", "Flood, water scarcity, illegal layouts, disputes &amp; dev-distance risks."), unsafe_allow_html=True)
    with fc8:
        st.markdown(_feature_card("🏘️", "Locality Data", "30+ cities with neighbourhood-level rates, pin codes &amp; landmarks."), unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    # How to Get Started
    st.markdown("### 🚀 How to Get Started")
    st.markdown("")

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(_step_card("1", "Pick a State & City", "Use the sidebar to select your target State/UT and City — or explore any area/locality."), unsafe_allow_html=True)
    with s2:
        st.markdown(_step_card("2", "Navigate the Sections", "Click any page in the sidebar menu to explore rates, predictions, maps, legal checks, and more."), unsafe_allow_html=True)
    with s3:
        st.markdown(_step_card("3", "Make Informed Decisions", "Compare cities, estimate costs, check legal risks — all backed by data across 200+ locations."), unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    # Top 10 Cities
    st.markdown("### 🏅 Top 10 Cities by Current Rate")
    top10 = latest_df.nlargest(10, "Rate_Per_SqFt")[["Location", "Rate_Per_SqFt", "Annual_Growth_Pct", "Infrastructure_Score", "Zone_Type"]].copy()
    top10.columns = ["City", "Rate (₹/sqft)", "Growth %", "Infra Score", "Zone Type"]
    top10["Rate (₹/sqft)"] = top10["Rate (₹/sqft)"].apply(lambda v: f"₹{v:,.0f}")
    top10 = top10.reset_index(drop=True)
    top10.index = top10.index + 1
    st.dataframe(top10, use_container_width=True)

    st.markdown("")

    # Mini Map
    st.markdown("### 🗺️ Quick Glance — India Land Rate Map")
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
    fig_mini.update_layout(map_style="carto-positron", height=480, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_mini, use_container_width=True)


# ═══════════════════════════════════════════
#  📍  LOCATION OVERVIEW
# ═══════════════════════════════════════════
elif page == "📍 Location Overview":

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
    else:
        st.warning("No data available for this location.")


# ═══════════════════════════════════════════
#  📈  RATE PREDICTION
# ═══════════════════════════════════════════
elif page == "📈 Rate Prediction":

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
elif page == "🗺️ Interactive Map":

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
elif page == "⚖️ Compare Locations":

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
elif page == "💰 Investment Calculator":

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
elif page == "🛡️ Legal Risk Checker":

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
elif page == "🚨 Area Risk Alerts":

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

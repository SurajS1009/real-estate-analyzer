"""
India Land Rate Prediction Engine
===================================
ML-based prediction for future land rates across India.
Uses Polynomial Regression with confidence intervals.
All values in Indian Rupees (₹).
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def predict_future_rates(df, location, years_ahead=5):
    """Predict future land rates using Polynomial Regression."""
    loc_data = df[df["Location"] == location].sort_values("Year")
    if loc_data.empty or len(loc_data) < 3:
        return None

    X = loc_data["Year"].values.reshape(-1, 1)
    y = loc_data["Rate_Per_SqFt"].values

    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)

    r2 = r2_score(y, model.predict(X_poly))

    last_year = int(loc_data["Year"].max())
    future_years = np.array(range(last_year + 1, last_year + 1 + years_ahead)).reshape(-1, 1)
    future_poly = poly.transform(future_years)
    predictions = model.predict(future_poly)

    residuals = y - model.predict(X_poly)
    std_err = np.std(residuals)

    results = []
    for i, yr in enumerate(future_years.flatten()):
        pred = max(predictions[i], y[-1] * 0.9)
        margin = std_err * 1.96 * (1 + 0.1 * (i + 1))
        results.append({
            "Year": int(yr),
            "Predicted_Rate": round(pred, 2),
            "Lower_Bound": round(max(pred - margin, 0), 2),
            "Upper_Bound": round(pred + margin, 2),
            "Confidence": round(max(0.5, min(0.95, r2 - 0.02 * (i + 1))), 2),
        })

    return {
        "location": location,
        "model_r2": round(r2, 4),
        "current_rate": round(y[-1], 2),
        "predictions": pd.DataFrame(results),
        "historical": loc_data[["Year", "Rate_Per_SqFt"]],
    }


def calculate_investment_roi(df, location, investment_amount, years):
    """Calculate projected ROI for a land investment in ₹."""
    prediction = predict_future_rates(df, location, years)
    if prediction is None:
        return None

    current_rate = prediction["current_rate"]
    area_sqft = investment_amount / current_rate

    results = []
    for _, row in prediction["predictions"].iterrows():
        future_value = area_sqft * row["Predicted_Rate"]
        profit = future_value - investment_amount
        roi_pct = (profit / investment_amount) * 100
        annualized_roi = ((future_value / investment_amount) ** (1 / max(row["Year"] - 2026, 1)) - 1) * 100
        results.append({
            "Year": row["Year"],
            "Projected_Value_₹": round(future_value, 2),
            "Profit_₹": round(profit, 2),
            "ROI_Pct": round(roi_pct, 2),
            "Annualized_ROI_Pct": round(annualized_roi, 2),
            "Rate_Per_SqFt": row["Predicted_Rate"],
        })

    return {
        "location": location,
        "investment_₹": investment_amount,
        "area_sqft": round(area_sqft, 2),
        "current_rate": current_rate,
        "projections": pd.DataFrame(results),
    }


def get_development_forecast(df, location, dev_factors):
    """Generate comprehensive development forecast for a location."""
    loc_data = df[df["Location"] == location]
    if loc_data.empty:
        return None

    latest = loc_data.sort_values("Year").iloc[-1]
    zone_type = latest["Zone_Type"]
    factor = dev_factors.get(zone_type, dev_factors.get("Tier-2 City", {}))

    infra = latest["Infrastructure_Score"]
    dev_pot = latest["Development_Potential"]
    growth = latest["Annual_Growth_Pct"]

    overall_score = (
        infra * 0.3
        + dev_pot * 0.3
        + min(growth * 8, 100) * 0.2
        + factor.get("growth_multiplier", 1.0) * 50 * 0.2
    )

    if overall_score >= 75:
        outlook = "🟢 Excellent"
    elif overall_score >= 60:
        outlook = "🟡 Good"
    elif overall_score >= 45:
        outlook = "🟠 Moderate"
    else:
        outlook = "🔴 Below Average"

    return {
        "location": location,
        "zone_type": zone_type,
        "description": factor.get("description", "N/A"),
        "growth_multiplier": factor.get("growth_multiplier", 1.0),
        "risk_level": factor.get("risk_level", "Unknown"),
        "key_drivers": factor.get("key_drivers", []),
        "forecast": factor.get("forecast", "N/A"),
        "infrastructure_score": infra,
        "development_potential": dev_pot,
        "overall_score": round(overall_score, 1),
        "outlook": outlook,
        "current_rate": latest["Rate_Per_SqFt"],
        "growth_rate": growth,
    }


def compare_locations(df, locations, dev_factors):
    """Compare multiple Indian locations side by side."""
    comparisons = []
    for loc in locations:
        loc_data = df[df["Location"] == loc]
        if loc_data.empty:
            continue
        latest = loc_data.sort_values("Year").iloc[-1]
        earliest = loc_data.sort_values("Year").iloc[0]
        total_growth = ((latest["Rate_Per_SqFt"] - earliest["Rate_Per_SqFt"]) / earliest["Rate_Per_SqFt"]) * 100
        n_years = max(latest["Year"] - earliest["Year"], 1)
        cagr = ((latest["Rate_Per_SqFt"] / earliest["Rate_Per_SqFt"]) ** (1 / n_years) - 1) * 100

        zone_type = latest["Zone_Type"]
        factor = dev_factors.get(zone_type, {})

        prediction = predict_future_rates(df, loc, 5)
        pred_5yr = prediction["predictions"].iloc[-1]["Predicted_Rate"] if prediction else None

        comparisons.append({
            "Location": loc,
            "Current_Rate_₹": round(latest["Rate_Per_SqFt"], 2),
            "CAGR_%": round(cagr, 2),
            "Total_Growth_%": round(total_growth, 2),
            "Zone_Type": zone_type,
            "Infra_Score": latest["Infrastructure_Score"],
            "Dev_Potential": latest["Development_Potential"],
            "Risk": factor.get("risk_level", "Unknown"),
            "5Yr_Predicted_₹": round(pred_5yr, 2) if pred_5yr else None,
            "Growth_Multiplier": factor.get("growth_multiplier", 1.0),
        })

    return pd.DataFrame(comparisons)

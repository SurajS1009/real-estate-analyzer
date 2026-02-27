# 🏠 India Land Rate Analyzer & Predictor

A comprehensive Streamlit web application for understanding land rates across India, predicting future prices, and assessing legal & environmental risks.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

| Tab | Description |
|-----|-------------|
| 📍 **Location Overview** | Current land rates, growth trends, infrastructure scores for 200+ Indian cities |
| 📈 **Rate Prediction** | ML-powered future rate forecasting with confidence intervals |
| 🗺️ **Interactive Map** | Pan-India map visualization of land rates and growth hotspots |
| ⚖️ **Compare Locations** | Side-by-side comparison of up to 5 cities |
| 💰 **Investment Calculator** | ROI projections for land investment scenarios |
| 🛡️ **Legal Risk Checker** | State-specific land laws, RERA status, stamp duty, CRZ & tribal restrictions |
| 🚨 **Area Risk Alerts** | Flood risk, water scarcity, illegal layouts, land disputes, proximity analysis |

## 📊 Coverage

- **28 States + 8 Union Territories**
- **200+ Cities, Towns & Zones**
- **80+ Zone Types** (IT Corridor, SEZ, Heritage, Industrial, etc.)
- **City-level CRZ & Tribal overrides** for accurate coastal/tribal data

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/land-rate-app-india.git
cd land-rate-app-india

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501**

## 🏗️ Project Structure

```
land_rate_app/
├── app.py                  # Main Streamlit application (7 tabs)
├── data_module.py          # India land rate dataset, legal data, risk alerts
├── prediction_engine.py    # ML prediction engine (Polynomial Regression)
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Charts & Maps**: Plotly (scatter_map, gauges, radar charts)
- **ML**: scikit-learn (Polynomial Regression)
- **Data**: Pandas, NumPy

## 📸 Screenshots

> Run the app locally to explore all 7 tabs!

## ⚠️ Disclaimer

This app provides **indicative/educational** land rate data. Actual land prices vary by locality, time, and market conditions. Always consult local real estate professionals and verify with government records before making investment decisions.

## 📄 License

MIT License – free to use, modify, and distribute.

---

Built with ❤️ using Streamlit & Python

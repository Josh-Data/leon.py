# app.py
import streamlit as st
import yfinance as yf
from causalimpact import CausalImpact
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from datetime import datetime, timedelta

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }
    .css-1d391kg {
        background-color: white;
    }
    .stButton>button {
        background-color: #4addbe;
        color: white;
        border: 1px solid #2c3e50 !important;
    }
    .stMarkdown, h1, h2, h3, p, span, label {
        color: #2c3e50 !important;
    }
    .st-emotion-cache-1y4p8pa {
        width: 100%;
    }
    .st-emotion-cache-1y4p8pa .stSlider > div > div > div {
        background-color: #4addbe !important;
    }
    .st-emotion-cache-1y4p8pa .stSlider > div > div > div > div {
        background-color: #4addbe !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Stock Causal Impact Analysis")

# Date inputs
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start Date", value=datetime(2023, 11, 13))
    treatment_start = st.date_input("Treatment Start Date", value=datetime(2024, 11, 11))
with col2:
    training_end = st.date_input("Training End Date", value=datetime(2024, 11, 8))
    treatment_end = st.date_input("Treatment End Date", value=datetime(2024, 11, 14))

# Stock selection
target_stock = st.text_input("Target Stock Symbol", value="TSLA")
stocks = st.multiselect(
    "Control Stocks",
    ["WMT", "DIS", "NVS", "MSFT", "META", "XOM", "NVDA", "SBUX"],
    default=["WMT", "DIS", "MSFT", "META", "NVDA", "SBUX"]
)

if st.button("Run Analysis", key="run_analysis"):
    try:
        # Download target stock data
        y = yf.download(target_stock, start=start, end=treatment_end + timedelta(days=1), interval="1d")
        y = y["Close"]

        # Download control stocks data
        X = yf.download(tickers=stocks, start=start, end=treatment_end + timedelta(days=1), interval="1D")
        X = X["Close"]

        # Combine data
        df = pd.concat([y, X], axis=1).dropna()
        
        # Training data for stationarity test
        df_train = df[start:treatment_start]
        
        # Stationarity tests
        st.subheader("Stationarity Tests")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Original Data")
            adf_result = adfuller(df_train[target_stock])
            st.write(f"ADF Statistic: {adf_result[0]:.4f}")
            st.write(f"p-value: {adf_result[1]:.4f}")
        
        with col2:
            st.write("Differenced Data")
            diff = df_train.pct_change().dropna()
            adf_result_diff = adfuller(diff[target_stock])
            st.write(f"ADF Statistic: {adf_result_diff[0]:.4f}")
            st.write(f"p-value: {adf_result_diff[1]:.4f}")

        # Correlation heatmap
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(diff.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
        st.pyplot(fig)
        plt.close()

        # Causal Impact Analysis
        pre_period = [start.strftime('%Y-%m-%d'), training_end.strftime('%Y-%m-%d')]
        post_period = [treatment_start.strftime('%Y-%m-%d'), treatment_end.strftime('%Y-%m-%d')]
        
        impact = CausalImpact(data=df, pre_period=pre_period, post_period=post_period)
        
        # Plot causal impact
        st.subheader("Causal Impact Analysis")
        impact_fig = impact.plot()
        st.pyplot(impact_fig)
        plt.close()

        # Summary report
        st.subheader("Impact Summary Report")
        st.text(impact.summary("report"))

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        
        

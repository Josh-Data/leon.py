import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS
from scipy import stats
import datetime

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

class CausalImpactAnalysis:
    def __init__(self, data, pre_period, post_period):
        self.data = data
        self.pre_period = pre_period
        self.post_period = post_period
        self.target = data.iloc[:, 0]
        self.controls = data.iloc[:, 1:]
        self.fit_model()
        
    def fit_model(self):
        # Split data into pre and post periods
        mask_pre = (self.data.index >= self.pre_period[0]) & (self.data.index <= self.pre_period[1])
        mask_post = (self.data.index >= self.post_period[0]) & (self.data.index <= self.post_period[1])
        
        # Fit model on pre-period
        X_pre = self.controls[mask_pre]
        y_pre = self.target[mask_pre]
        self.model = OLS(y_pre, X_pre).fit()
        
        # Generate predictions for entire period
        X_all = self.controls
        self.predictions = self.model.predict(X_all)
        
        # Calculate point-wise confidence intervals
        self.alpha = 0.05  # 95% confidence interval
        X_post = self.controls[mask_post]
        
        # Calculate standard error of forecast
        self.sigma = np.sqrt(self.model.mse_resid)
        self.forecast_var = self.sigma**2 * (1 + np.diag(X_post.dot(np.linalg.inv(X_pre.T.dot(X_pre))).dot(X_post.T)))
        self.ci_lower = self.predictions[mask_post] - stats.norm.ppf(1 - self.alpha/2) * np.sqrt(self.forecast_var)
        self.ci_upper = self.predictions[mask_post] + stats.norm.ppf(1 - self.alpha/2) * np.sqrt(self.forecast_var)
        
        # Calculate cumulative impact
        self.actual_post = self.target[mask_post]
        self.predicted_post = self.predictions[mask_post]
        self.impact = self.actual_post - self.predicted_post
        self.cumulative_impact = self.impact.sum()
        
        # Calculate p-value
        t_stat = self.cumulative_impact / (self.sigma * np.sqrt(len(self.actual_post)))
        self.p_value = 2 * (1 - stats.norm.cdf(abs(t_stat)))
        
        # Calculate relative effect
        self.relative_effect = self.cumulative_impact / self.predicted_post.sum()
        
    def plot(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
        
        # Original vs Predicted
        ax1.plot(self.data.index, self.target, label='Observed', color='black')
        ax1.plot(self.data.index, self.predictions, label='Predicted', color='blue', linestyle='--')
        ax1.axvline(x=self.post_period[0], color='red', linestyle='--')
        ax1.fill_between(self.data.index[self.data.index >= self.post_period[0]],
                        self.ci_lower,
                        self.ci_upper,
                        alpha=0.1, color='blue')
        ax1.set_title('Original vs Predicted')
        ax1.legend()
        
        # Pointwise Impact
        impact_series = self.target - self.predictions
        ax2.plot(self.data.index, impact_series, label='Impact', color='blue')
        ax2.axvline(x=self.post_period[0], color='red', linestyle='--')
        ax2.axhline(y=0, color='gray', linestyle='-')
        ax2.set_title('Pointwise Impact')
        
        # Cumulative Impact
        cumulative_impact = impact_series.cumsum()
        ax3.plot(self.data.index, cumulative_impact, label='Cumulative Impact', color='blue')
        ax3.axvline(x=self.post_period[0], color='red', linestyle='--')
        ax3.axhline(y=0, color='gray', linestyle='-')
        ax3.set_title('Cumulative Impact')
        
        plt.tight_layout()
        return fig
        
    def summary(self, output='report'):
        absolute_effect = self.cumulative_impact
        relative_effect = self.relative_effect * 100
        
        report = f"""
Causal Impact Analysis Report
============================

During the post-intervention period, the response variable had
an average value of approximately {self.actual_post.mean():.2f}.
By contrast, in the absence of an intervention, we would have expected 
an average value of {self.predicted_post.mean():.2f}.

The intervention caused a {relative_effect:.1f}% {'increase' if relative_effect > 0 else 'decrease'} in the response variable.
The absolute effect was {absolute_effect:.2f}.

The statistical significance of this effect is p = {self.p_value:.3f}.
This means the likelihood of obtaining this effect by chance is {'very small' if self.p_value < 0.05 else 'not negligible'}.

Interpretation:
{' - Causal impact DETECTED (95% confidence)' if self.p_value < 0.05 else ' - Causal impact NOT DETECTED (95% confidence)'}
"""
        return report

# Streamlit app
st.title("Stock Causal Impact Analysis")

# Date inputs
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start Date", value=datetime.datetime(2023, 11, 13))
    treatment_start = st.date_input("Treatment Start Date", value=datetime.datetime(2024, 11, 11))
with col2:
    training_end = st.date_input("Training End Date", value=datetime.datetime(2024, 11, 8))
    treatment_end = st.date_input("Treatment End Date", value=datetime.datetime(2024, 11, 14))

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
        y = yf.download(target_stock, start=start, end=treatment_end + datetime.timedelta(days=1), interval="1d")
        y = y["Close"]

        # Download control stocks data
        X = yf.download(tickers=stocks, start=start, end=treatment_end + datetime.timedelta(days=1), interval="1D")
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
        pre_period = [start, training_end]
        post_period = [treatment_start, treatment_end]
        
        impact = CausalImpactAnalysis(data=df, pre_period=pre_period, post_period=post_period)
        
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
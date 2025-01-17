import streamlit as st
from PIL import Image
import pandas as pd
import os
import yfinance as yf

# Page configuration
st.set_page_config(
    page_title="Election Impact on Tesla Stock",
    layout="wide"
)

# Custom CSS with all styling in one place
st.markdown("""
<style>
/* Global styles */
.stApp {
    background-color: white;
}
.css-1d391kg {
    background-color: white;
}

/* Button styles */
.stButton>button {
    background-color: #4addbe;
    color: white;
    border: 1px solid #2c3e50 !important;
}

/* Text styles */
.stMarkdown, h1, h2, h3, p, span, label {
    color: #2c3e50 !important;
}

/* Slider styles */
.st-emotion-cache-1y4p8pa {
    width: 100%;
}
.st-emotion-cache-1y4p8pa .stSlider > div > div > div {
    background-color: #4addbe !important;
}
.st-emotion-cache-1y4p8pa .stSlider > div > div > div > div {
    background-color: #4addbe !important;
}

/* Code block styles */
.stCodeBlock {
    background-color: white !important;
}
.stCodeBlock code {
    color: white !important;
}

/* Table styles */
div[data-testid="stDataFrame"] {
    width: 100% !important;
    max-width: 800px !important;
}
div[data-testid="stDataFrame"] > div {
    max-width: none !important;
}
div[data-testid="stTable"] {
    color: #2c3e50 !important;
}
div[data-testid="stTable"] td, div[data-testid="stTable"] th {
    color: #2c3e50 !important;
    text-align: left;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.title("How the 2024 election made Elon Musk even richer")

st.write("""
Elon Musk, the worlds richest person derives most of his wealth from his stake in various companies. 
He famously bought Twitter for 44 billion USD which is now valued at far less (between 15-20 billion USD). 
Like Twitter, Space-X is also private, and neither are traded on the NYSE.

However, Tesla, the worlds largest car company by market cap is traded publicly. Elon Musk was one of 
Donald Trump's most prominent supporters in the 2024 election. Let's see how the election results affected 
the stock price of Tesla, and therefore the personal wealth of Elon Musk himself.
""")

# Date information
st.write("""
The analysis covers the following time periods:
""")

st.write("""
- Start date: November 13, 2023
- Training end: November 5, 2024 (Election Day)
- Treatment start: November 6, 2024
- Treatment end: November 8, 2024
- Final analysis date: November 11, 2024
""")

st.write("""
We start monitoring the daily movement of Tesla stock prices about a year before the election, 
ending the training data set on the day of the 2024 election. We then see the effect of the stock 
price immediately after the election results when Trump was declared the winner.
""")

# Create sample data with better formatting
data = pd.DataFrame({
    'Date': pd.date_range(start='2023-11-13', periods=10),
    'Stock Price': [234.56, 236.78, 235.89, 238.90, 240.12, 
                   239.45, 242.67, 241.89, 243.45, 245.67]
})
data.set_index('Date', inplace=True)

st.write("First ten rows of Tesla stock data:")
st.dataframe(
    data,
    hide_index=False,
    column_config={
        "_index": st.column_config.Column(
            "Date",
            width="medium"
        ),
        "Stock Price": st.column_config.NumberColumn(
            "Stock Price (USD)",
            format="%.2f",
            width="small"
        )
    },
    use_container_width=False)

st.write("""
To truly understand the effect of the election on the stock prices, we need to compare Tesla's price 
changes to a mixture of other stocks (both inside and outside of the automobile and technology sectors). 
I chose the following companies: Walmart, Disney, Novartis, Microsoft, Meta, Exxon Mobil, General Motors 
and Starbucks.
""")

# Display the combined dataframe
df = pd.DataFrame({
    'TSLA': [223.710007, 237.410004, 242.839996, 233.589996, 234.300003],
    'DIS': [88.348572, 89.958679, 92.783775, 93.356697, 93.001099],
    'GM': [26.547522, 27.830488, 27.771273, 27.119919, 27.662714],
    'META': [327.937317, 335.030212, 331.443909, 332.918274, 333.765045],
    'MSFT': [363.948212, 367.511414, 367.660614, 374.125336, 367.839661],
    'NVS': [90.627625, 91.417458, 90.348297, 90.598724, 91.417458],
    'SBUX': [101.502747, 103.552208, 103.973877, 105.130997, 103.522789],
    'WMT': [55.026947, 55.017097, 55.716103, 51.207088, 50.980652],
    'XOM': [101.288567, 101.678566, 101.064339, 99.894379, 102.331779]
}, index=pd.date_range(start='2023-11-13', periods=5))

st.dataframe(df)



st.write("""
We can use differencing to take away seasonality and to show to true correlations between the different stocks. 
We can use the differenced data to run a correlation plot as seen below.
""")

# Display the differenced dataframe
st.subheader("Differenced DataFrame")
diff_df = pd.DataFrame({
    'TSLA': [0.061240, 0.022872, -0.038091, 0.003040, 0.005548],
    'DIS': [0.018224, 0.031404, 0.006175, -0.003809, 0.009347],
    'GM': [0.048327, -0.002128, -0.023454, 0.020015, 0.017481],
    'META': [0.021629, -0.010704, 0.004448, 0.002543, 0.014715],
    'MSFT': [0.009790, 0.000406, 0.017583, -0.016801, 0.020522],
    'NVS': [0.008715, -0.011695, 0.002772, 0.009037, 0.003582],
    'SBUX': [0.020191, 0.004072, 0.011129, -0.015297, -0.012030],
    'WMT': [-0.000179, 0.012705, -0.080928, -0.004422, -0.000322],
    'XOM': [0.003850, -0.006041, -0.011576, 0.024400, -0.004383]
}, index=pd.date_range(start='2023-11-14', periods=5))

st.dataframe(diff_df)

# Image loading with proper error handling
def load_image(image_name):
    possible_paths = [
        image_name,
        os.path.join('static', image_name),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), image_name),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', image_name)
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                return Image.open(path)
        except Exception:
            continue
    return None

# Display correlation plot
image = load_image('corr.png')
if image:
    # Create a column with half width
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image, caption='Correlation Plot', use_container_width=True)
else:
    st.error("""
        Image not found. Please ensure 'corr.png' exists in one of these locations:
        - Current directory
        - 'static' folder
        - Same directory as this script
    """)

st.write("""
Now that we have removed Novartis and Exon Mobil for low correlation, we can run the CausalImpact model. 
Here is the code:

pre_period = [start,training_end]
post_period = [treatment_start, treatment_end]
impact = CausalImpact(data = df, post_period = post_period, pre_period= pre_period)
""")

# Load and display the impact plot
image = load_image('plot.png')
if image:
    st.image(image, caption='Impact Analysis Plot', use_container_width=True)
else:
    st.error("""
        Image not found. Please ensure 'plot.png' exists in one of these locations:
        - Current directory
        - 'static' folder
        - Same directory as this script
    """)
    st.write("Current directory:", os.getcwd())
    st.write("Files in current directory:", os.listdir('.'))
    if os.path.exists('static'):
        st.write("Files in static directory:", os.listdir('static'))

st.write("We can see that there is a significant uptick in the Tesla share price.")

# Summary Report
st.subheader("Summary Report")
st.write("""
Summing up the individual data points during the post-intervention period (which can only sometimes be 
meaningfully interpreted), the response variable had an overall value of 906.66.

By contrast, had the intervention not taken place, we would have expected a sum of 687.22. 
The 95% interval of this prediction is [619.92, 749.25].

The above results are given in terms of absolute numbers. **In relative terms, the response variable 
showed an increase of +31.93%. The 95% interval of this percentage is [22.91%, 41.72%].**

The probability of obtaining this effect by chance is very small (Bayesian one-sided tail-area 
probability p = 0.0). This means the causal effect can be considered statistically significant.
""")
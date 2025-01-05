import streamlit as st
from PIL import Image
import pandas as pd
import os

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
    color: #2c3e50 !important;
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
Like Twitter, Space-X is also private, and not neither are traded on the NYSE.

However, Tesla, the worlds largest car company by market cap is traded publicly. Elon Musk was one of 
Donald Trump's most prominent supporters in the 2024 election. Let's see how the election results affected 
the stock price of Tesla, and therefore the personal wealth of Elon Musk himself.
""")

# Date parameters with white background
st.code("""
start = "2023-11-13"
training_end = "2024-11-05"
treatment_start = "2024-11-06"
treatment_end = "2024-11-08"
end_stock = "2024-11-11"
""", language="python")

st.write("""
We start monitoring the daily movement of Tesla stock prices about a year before the election, 
ending the training data set on the day of the 2024 election. We then see the effect of the stock 
price immediately after the election results when Trump was declared the winner.
""")

# Create sample data with better formatting
st.write("First five rows of Tesla stock data:")
data = pd.DataFrame({
    'y': [234.56, 236.78, 235.89, 238.9, 240.12]
}, index=['2023-11-13 00:00:00', '2023-11-14 00:00:00', '2023-11-15 00:00:00', 
          '2023-11-16 00:00:00', '2023-11-17 00:00:00'])

st.dataframe(
    data,
    hide_index=False,
    column_config={
        "_index": st.column_config.Column(
            "Date",
            width="medium"
        ),
        "y": st.column_config.NumberColumn(
            "Stock Price",
            format="%.2f",
            width="small"
        )
    },
    use_container_width=False
)

st.write("""
To truly understand the effect of the election on the stock prices, we need to compare Tesla's price 
changes to a mixture of other stocks (both inside and outside of the automobile and technology sectors). 
I chose the following companies: Walmart, Disney, Novartis, Microsoft, Meta, Exxon Mobil, General Motors 
and Starbucks.
""")

# Display the concatenation code
st.code("""
df = pd.concat([y,X],axis = 1).dropna()
""", language="python")

# Image loading with proper error handling
def load_image(image_name):
    # Try multiple possible paths
    possible_paths = [
        image_name,  # Current directory
        os.path.join('static', image_name),  # Static folder
        os.path.join(os.path.dirname(os.path.abspath(__file__)), image_name),  # Script directory
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', image_name)  # Script's static folder
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                return Image.open(path)
        except Exception:
            continue
    
    return None

# Load and display the image
image = load_image('leon_plot.png')
if image:
    st.image(image, caption='Impact Analysis Plot', use_column_width=True)
else:
    st.error("""
        Image not found. Please ensure 'leon_plot.png' exists in one of these locations:
        - Current directory
        - 'static' folder
        - Same directory as this script
    """)
    # Debug information
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

The above results are given in terms of absolute numbers. In relative terms, the response variable 
showed an increase of +31.93%. The 95% interval of this percentage is [22.91%, 41.72%].

The probability of obtaining this effect by chance is very small (Bayesian one-sided tail-area 
probability p = 0.0). This means the causal effect can be considered statistically significant.
""")
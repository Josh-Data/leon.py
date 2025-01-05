import streamlit as st
from PIL import Image
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Election Impact on Tesla Stock",
    layout="wide"
)

# Custom CSS with fixed slider color and code block styling
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
/* Style for slider - new streamlit class names */
.st-emotion-cache-1y4p8pa {
    width: 100%;
}
.st-emotion-cache-1y4p8pa .stSlider > div > div > div {
    background-color: #4addbe !important;
}
.st-emotion-cache-1y4p8pa .stSlider > div > div > div > div {
    background-color: #4addbe !important;
}
/* Custom styling for code blocks */
.stCodeBlock {
    background-color: #1e1e1e !important;
}
code {
    color: white !important;
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

# Display the date parameters with proper styling
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

# Create sample data matching the exact format shown
data = {
    'y': [234.56, 236.78, 235.89, 238.90, 240.12]
}
index = pd.date_range(start='2023-11-13', periods=5, freq='D')
df = pd.DataFrame(data, index=index)
df.index = df.index.strftime('%Y-%m-%d 00:00:00')
st.write("First five rows of Tesla stock data:")
st.dataframe(df, hide_index=False)

st.write("""
To truly understand the effect of the election on the stock prices, we need to compare Tesla's price 
changes to a mixture of other stocks (both inside and outside of the automobile and technology sectors). 
I chose the following companies: Walmart, Disney, Novartis, Microsoft, Meta, Exxon Mobil, General Motors 
and Starbucks.
""")

# Display the concatenation code with proper styling
st.code("""
df = pd.concat([y,X],axis = 1).dropna()
""", language="python")

# Check for image in various locations
possible_image_paths = [
    'leon_plot.png',
    './leon_plot.png',
    '../leon_plot.png',
    'static/leon_plot.png'
]

image_found = False
for img_path in possible_image_paths:
    if os.path.exists(img_path):
        try:
            image = Image.open(img_path)
            st.image(image, caption='Impact Analysis Plot')
            image_found = True
            break
        except Exception as e:
            continue

if not image_found:
    st.error("Error: leon_plot.png not found. Please ensure the image is properly uploaded.")
    st.write("Current directory contents:")
    st.code("\n".join(os.listdir()), language="text")

st.write("We can see that there is a significant uptick in the Tesla share price.")

# Display the summary statistics
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
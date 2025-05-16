import streamlit as st
import pandas as pd
from scripts.fetch_trends import fetch_google_trends
from scripts.preprocess import preprocess_m5_sales, preprocess_m5_by_item
from scripts.forecasting import forecast_trends, forecast_sales_m5
from scripts.visualization import plot_trend, plot_forecast, plot_sales_forecast
import gdown

st.set_page_config(layout="wide")
st.title("📊 E-commerce Demand Forecasting Dashboard")

keywords = ["iPhone", "PS5", "Air Jordan", "Instant Pot", "Samsung Galaxy"]

# Fetch Trends
data = fetch_google_trends(keywords)

# M5 sales data
url = "https://drive.google.com/uc?id=161L9tY35hlis-pyiEfEGL1wDRR6n7MuQ"
output_path = "sales_train_validation.csv"

if not os.path.exists(output_path):
    gdown.download(url, output_path, quiet=False)

# Step 3: Load the data
sales_data = preprocess_m5_sales(output_path)

# Show Google Trends
tab1, tab2, tab3 = st.tabs(["📈 Trends", "🔮 Forecast", "🏪 Walmart Sales"])

with tab1:
    st.subheader("Google Search Trends")
    for keyword in keywords:
        fig = plot_trend(data, keyword)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Forecasts from Trends")
    for keyword in keywords:
        forecast, mape = forecast_trends(data, keyword, return_error=True)
        
        st.markdown(f"**{keyword}** — MAPE: `{mape:.2f}%`")
        fig = plot_forecast(forecast)
        st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.subheader("Walmart Sales Forecast (M5 Dataset)")
    forecast_sales, mape = forecast_sales_m5(sales_data, return_error=True)
    st.metric("MAPE", f"{mape:.2f}%")
    fig = plot_sales_forecast(forecast_sales)
    st.plotly_chart(fig, use_container_width=True)



st.success("Dashboard loaded successfully.")

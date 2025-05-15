import plotly.express as px

def plot_trend(data, keyword):
    fig = px.line(data, x='date', y=keyword, title=f'Trend for {keyword}')
    return fig

def plot_forecast(forecast):
    fig = px.line(forecast, x='ds', y='yhat')
    return fig

def plot_sales_forecast(forecast):
    fig = px.line(forecast, x='ds', y='yhat', title='M5 Walmart Sales Forecast')
    return fig
from prophet import Prophet
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error

def forecast_trends(data, keyword, return_error=False):
    df = data[['date', keyword]].rename(columns={'date': 'ds', keyword: 'y'})
    model = Prophet()
    model.fit(df)

    # Future range
    future_dates = pd.date_range(start='2025-01-01', end='2030-12-31', freq='D')
    future = pd.DataFrame({'ds': future_dates})
    forecast = model.predict(future)

    if return_error:
        # Evaluate only on training data
        history = model.predict(df[['ds']])
        mape = evaluate_forecast(df['y'], history['yhat'].clip(lower=0))
        return forecast, mape

    return forecast


def evaluate_forecast(y_true, y_pred):
    return mean_absolute_percentage_error(y_true, y_pred) * 100



def forecast_sales_m5(sales_df, return_error=False):
    df = sales_df.rename(columns={'Date': 'ds', 'sales': 'y'})

    # Optional: Clip negative/huge spikes
    df['y'] = df['y'].clip(lower=0)

    # Create and tune the model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,  # More flexible trend changes
        seasonality_mode='multiplicative',  # Try 'additive' if better
    )

    model.fit(df)

    # Forecast up to 2030
    last_date = df['ds'].max()
    future = model.make_future_dataframe(periods=(2030 - last_date.year) * 365)

    forecast = model.predict(future)

    if return_error:
        merged = pd.merge(df, forecast[['ds', 'yhat']], on='ds', how='left')
        mape = evaluate_forecast(merged['y'], merged['yhat'].clip(lower=0))
        return forecast, mape

    return forecast

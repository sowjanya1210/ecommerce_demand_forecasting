import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import time

@st.cache_data(ttl=86400)  # cache for 1 day
def fetch_google_trends(keywords, timeframe='today 5-y', geo='US'):
    time.sleep(5)  # small delay before calling
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
    data = pytrends.interest_over_time()
    if 'isPartial' in data.columns:
        data = data.drop(columns=['isPartial'])
    data.reset_index(inplace=True)
    return data

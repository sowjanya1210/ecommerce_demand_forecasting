from pytrends.request import TrendReq
import pandas as pd
import time

def fetch_google_trends(keywords, timeframe='today 5-y', geo='US'):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
    data = pytrends.interest_over_time()
    if 'isPartial' in data.columns:
        data = data.drop(columns=['isPartial'])
    data.reset_index(inplace=True)
    time.sleep(5)
    return data
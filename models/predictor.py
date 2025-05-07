import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def fetch_data(symbol, period="6mo"):
    df = yf.download(symbol, period=period, interval="1d")
    return df

def train_and_predict(symbol):
    df = fetch_data(symbol)
    if len(df) < 30:
        return None, None, None
    df['Return'] = df['Close'].pct_change()
    df = df.dropna()
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['Close'].values
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    tomorrow = np.array([[len(df)]])
    pred = model.predict(tomorrow)[0]
    last_close = y[-1]
    if pred > last_close:
        rec = "Buy"
    elif pred < last_close:
        rec = "Sell"
    else:
        rec = "Hold"
    return float(pred), float(last_close), rec

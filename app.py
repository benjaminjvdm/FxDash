import streamlit as st
st.set_page_config(layout="wide")
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates

st.title("Real-Time Financial Dashboard")
st.set_page_config(page_title="FxDash", page_icon="💸")

# Define the symbols
symbols = ["GBPJPY=X", "AUDJPY=X", "BTC-USD"]

# Define the layout
col1, col2 = st.columns(2)

# Placeholder for charts
gbpjpy_chart = col1.empty()
audjpy_chart = col2.empty()
btcusd_chart = st.empty()

while True:
    # Fetch data for each symbol
    data = {}
    for symbol in symbols:
        data[symbol] = yf.download(symbol, period="1wk", interval="15m")

    # Create candlestick charts
    fig_gbpjpy, ax_gbpjpy = plt.subplots()
    gbpjpy_data = data["GBPJPY=X"].copy()

    # Filter data to last 24 hours
    gbpjpy_data = gbpjpy_data.iloc[-96:] 

    gbpjpy_data['Date'] = gbpjpy_data.index.map(mpl_dates.date2num)
    gbpjpy_values = [tuple(x) for x in gbpjpy_data[['Date', 'Open', 'High', 'Low', 'Close']].values]
    fig_gbpjpy, ax_gbpjpy = plt.subplots()
    ax_gbpjpy.set_facecolor('black')
    candlestick_ohlc(ax_gbpjpy, gbpjpy_values, width=0.0006, colorup='g', colordown='r')
    ax_gbpjpy.set_title("GBPJPY")
    ax_gbpjpy.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))

    # Calculate Quarter Theory levels
    last_price = gbpjpy_data['Close'].iloc[-1].item()
    nearest_quarter = round(last_price * 4) / 4
    upper_quarter = nearest_quarter + 0.250
    lower_quarter = nearest_quarter - 0.250

    # Overlay Quarter Theory levels
    ax_gbpjpy.axhline(upper_quarter, color='green', linestyle='--')
    ax_gbpjpy.text(x=gbpjpy_data['Date'].iloc[-1], y=upper_quarter, s=str(round(upper_quarter, 3)), color='green')
    ax_gbpjpy.axhline(lower_quarter, color='red', linestyle='--')
    ax_gbpjpy.text(x=gbpjpy_data['Date'].iloc[-1], y=lower_quarter, s=str(round(lower_quarter, 3)), color='red')

    # Calculate and overlay 50-period EMA
    ema_50 = data["GBPJPY=X"]['Close'].ewm(span=50).mean()
    ax_gbpjpy.plot(gbpjpy_data['Date'], ema_50.iloc[-96:], color='white', label='EMA 50')

    gbpjpy_chart.pyplot(fig_gbpjpy, use_container_width=True)

    audjpy_data = data["AUDJPY=X"].copy()
    audjpy_data['Date'] = audjpy_data.index.map(mpl_dates.date2num)

    # Filter data to last 24 hours
    audjpy_data = audjpy_data.iloc[-96:] 

    audjpy_values = [tuple(x) for x in audjpy_data[['Date', 'Open', 'High', 'Low', 'Close']].values]
    fig_audjpy, ax_audjpy = plt.subplots()
    ax_audjpy.set_facecolor('black')
    candlestick_ohlc(ax_audjpy, audjpy_values, width=0.0006, colorup='g', colordown='r')
    ax_audjpy.set_title("AUDJPY")
    ax_audjpy.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))

    # Calculate Quarter Theory levels
    last_price = audjpy_data['Close'].iloc[-1].item()
    nearest_quarter = round(last_price * 4) / 4
    upper_quarter = nearest_quarter + 0.250
    lower_quarter = nearest_quarter - 0.250

    # Overlay Quarter Theory levels
    ax_audjpy.axhline(upper_quarter, color='green', linestyle='--')
    ax_audjpy.text(x=audjpy_data['Date'].iloc[-1], y=upper_quarter, s=str(round(upper_quarter, 3)), color='green')
    ax_audjpy.axhline(lower_quarter, color='red', linestyle='--')
    ax_audjpy.text(x=audjpy_data['Date'].iloc[-1], y=lower_quarter, s=str(round(lower_quarter, 3)), color='red')

    # Calculate and overlay 50-period EMA
    ema_50 = data["AUDJPY=X"]['Close'].ewm(span=50).mean()
    ax_audjpy.plot(audjpy_data['Date'], ema_50.iloc[-96:], color='white', label='EMA 50')

    audjpy_chart.pyplot(fig_audjpy, use_container_width=True)

    btcusd_data = data["BTC-USD"].copy()
    btcusd_data = btcusd_data.iloc[-96:] 
    btcusd_data['Date'] = btcusd_data.index.map(mpl_dates.date2num)
    btcusd_values = [tuple(x) for x in btcusd_data[['Date', 'Open', 'High', 'Low', 'Close']].values]
    fig_btcusd, ax_btcusd = plt.subplots()
    ax_btcusd.set_facecolor('black')
    candlestick_ohlc(ax_btcusd, btcusd_values, width=0.0006, colorup='g', colordown='r')
    ax_btcusd.set_title("BTCUSD")
    ax_btcusd.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))

    # Kairi Relative Index (KRI) with Arrows
    length = 14  # From kairi.pine
    src = btcusd_data['Close']  # Source (close price)
    sma = src.rolling(window=length).mean()
    kri = 100 * (src - sma) / sma

    # Buy/Sell signals
    buySignal = pd.Series(False, index=btcusd_data.index)
    sellSignal = pd.Series(False, index=btcusd_data.index)
    for i in range(1, len(btcusd_data)):
        if kri.iloc[i-1].item() < 0 and kri.iloc[i].item() >= 0:
            buySignal.iloc[i] = True
        elif kri.iloc[i-1].item() > 0 and kri.iloc[i].item() <= 0:
            sellSignal.iloc[i] = True

    # Plot Buy/Sell signals
    ax_btcusd.plot(btcusd_data['Date'][buySignal.values], btcusd_data['Low'][buySignal.values], '^', markersize=5, color='green', label='Buy Signal')
    ax_btcusd.plot(btcusd_data['Date'][sellSignal.values], btcusd_data['High'][sellSignal.values], 'v', markersize=5, color='red', label='Sell Signal')

    btcusd_chart.pyplot(fig_btcusd, use_container_width=True)

    time.sleep(60)
    st.rerun()

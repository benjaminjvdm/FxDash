import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates

st.set_page_config(page_title="FxDash", page_icon="💸", layout="wide")
st.title("Real-Time Financial Dashboard")

# Define the symbols
symbols = ["GBPJPY=X", "AUDJPY=X", "GC=F"]

# Define the layout
col1, col2 = st.columns(2)

# Placeholder for charts
gbpjpy_chart = col1.empty()
audjpy_chart = col2.empty()
xauusd_chart = st.empty()

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

    audjpy_chart.pyplot(fig_audjpy, use_container_width=True)

    xauusd_data = data["GC=F"].copy()
    xauusd_data = xauusd_data.iloc[-96:] 
    xauusd_data['Date'] = xauusd_data.index.map(mpl_dates.date2num)
    xauusd_values = [tuple(x) for x in xauusd_data[['Date', 'Open', 'High', 'Low', 'Close']].values]
    fig_xauusd, ax_xauusd = plt.subplots()
    ax_xauusd.set_facecolor('black')
    candlestick_ohlc(ax_xauusd, xauusd_values, width=0.0006, colorup='g', colordown='r')
    ax_xauusd.set_title("xauusd")
    ax_xauusd.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))

    xauusd_chart.pyplot(fig_xauusd, use_container_width=True)

    time.sleep(60)
    st.rerun()
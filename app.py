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
symbols = ["GBPJPY=X"]
intervals = ["5m"]

# Define the layout
col1 = st.columns(1)[0]

# Placeholder for charts
gbpjpy_chart_5m = col1.empty()
#gbpjpy_chart_15m = col2.empty()
#gbpjpy_chart_1h = col3.empty()

while True:
    # Fetch data for each symbol
    data = {}
    for symbol in symbols:
        if symbol == "GBPJPY=X":
            for interval in intervals:
                try:
                    data[symbol + "_" + interval] = yf.download(symbol, period="1wk", interval=interval)
                except Exception as e:
                    print(f"Error downloading data for {symbol} {interval}: {e}")
                    time.sleep(60)  # Wait for 60 seconds before retrying
                    continue
                time.sleep(5)  # Add a 5-second delay between API calls 

    # Create candlestick charts for GBPJPY
    for interval in intervals:
        fig_gbpjpy, ax_gbpjpy = plt.subplots()
        gbpjpy_data = data["GBPJPY=X_" + interval].copy()

        # Filter data to last 24 hours
        if interval == "5m":
            gbpjpy_data = gbpjpy_data.iloc[-28:] # 24 hours * 60 minutes / 5 minutes
        #elif interval == "15m":
        #    gbpjpy_data = gbpjpy_data.iloc[-96:] # 24 hours * 60 minutes / 15 minutes
        #else:
        #    gbpjpy_data = gbpjpy_data.iloc[-24:] # 24 hours * 1 hour / 1 hour

    gbpjpy_data['Date'] = gbpjpy_data.index.map(mpl_dates.date2num)
    gbpjpy_values = [tuple(x) for x in gbpjpy_data[['Date', 'Open', 'High', 'Low', 'Close']].values]
    fig_gbpjpy, ax_gbpjpy = plt.subplots()
    ax_gbpjpy.set_facecolor('black')
    candlestick_ohlc(ax_gbpjpy, gbpjpy_values, width=0.0006, colorup='g', colordown='r')
    ax_gbpjpy.set_title(f"GBPJPY ({interval})")
    ax_gbpjpy.xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M'))



    if interval == "5m":
        gbpjpy_chart_5m.pyplot(fig_gbpjpy, use_container_width=True)
    #elif interval == "15m":
    #    gbpjpy_chart_15m.pyplot(fig_gbpjpy, use_container_width=True)
    #else:
    #    gbpjpy_chart_1h.pyplot(fig_gbpjpy, use_container_width=True)




    
        now = time.localtime()
        seconds_to_sleep = 60 - now.tm_sec
        time.sleep(seconds_to_sleep)
        st.rerun()

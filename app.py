import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="TradeGuru AI", layout="wide")
st.title("TradeGuru AI – Smart Buy/Sell Signals")
st.markdown("_Real-time signals for top stocks & crypto pairs._")

tickers = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC",
    "BA", "BABA", "DIS", "UBER", "LYFT", "SHOP", "SQ", "PYPL", "PLTR", "SNOW",
    "CRM", "ORCL", "QCOM", "AVGO", "TXN", "MRNA", "JNJ", "PFE", "XOM", "CVX",
    "KO", "PEP", "MCD", "WMT", "HD", "COST", "T", "VZ", "NKE", "SBUX", "WBA",
    "JPM", "BAC", "WFC", "MS", "MA", "AXP", "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD"
]

st.selectbox("Select a ticker:", tickers, key="selected_ticker")

@st.cache_data
def get_signal(ticker):
    df = yf.download(ticker, period="3mo", interval="1d")
    df.ta.rsi(length=14, append=True)
    return df

if st.session_state.selected_ticker:
    with st.spinner("Analyzing data..."):
        try:
            df = get_signal(st.session_state.selected_ticker)

            if "RSI_14" in df.columns:
                st.subheader(f"RSI Signal for {st.session_state.selected_ticker}")
                st.line_chart(df["RSI_14"].dropna())
            else:
                st.error("RSI_14 not found in the data. The ticker may be invalid or missing data.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

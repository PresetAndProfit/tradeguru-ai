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

ticker = st.selectbox("Select a ticker:", tickers)

@st.cache_data
def get_signal(ticker):
    df = yf.download(ticker, period="3mo", interval="1d")
    if df.empty:
        return None
    df.ta.rsi(length=14, append=True)
    return df

if ticker:
    with st.spinner("Analyzing data..."):
        df = get_signal(ticker)

        if df is None or "RSI_14" not in df.columns:
            st.error(f"Unable to compute RSI for {ticker}. Data may be missing or incomplete.")
        else:
            st.subheader(f"RSI Signal for {ticker}")
            st.line_chart(df["RSI_14"].dropna())

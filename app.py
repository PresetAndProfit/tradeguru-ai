import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="TradeGuru AI", layout="wide")
st.title("TradeGuru AI – Smart Buy/Sell Signals")
st.markdown("_Real-time signals for top stocks & crypto pairs._")

tickers = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC",
    "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD"
]

ticker = st.selectbox("Select a ticker:", tickers)

@st.cache_data
def fetch_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    if df.empty or len(df) < 20:
        return None
    df.ta.rsi(length=14, append=True)
    return df

if ticker:
    with st.spinner("Fetching and analyzing data..."):
        df = fetch_data(ticker)

        if df is None:
            st.error("Not enough data or data failed to load.")
        else:
            st.write("**Available columns:**", df.columns.tolist())  # Debug
            if "RSI_14" not in df.columns:
                st.error("RSI column not found after calculation.")
            else:
                st.subheader(f"RSI Indicator for {ticker}")
                st.line_chart(df["RSI_14"].dropna())
                latest_rsi = df["RSI_14"].dropna().iloc[-1]
                st.metric("Latest RSI", round(latest_rsi, 2))

                if latest_rsi < 30:
                    st.success("Buy signal: RSI is below 30 (oversold)")
                elif latest_rsi > 70:
                    st.error("Sell signal: RSI is above 70 (overbought)")
                else:
                    st.info("Hold: RSI is in the neutral range (30-70)")

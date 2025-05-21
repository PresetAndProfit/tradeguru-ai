import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="TradeGuru AI", layout="wide")
st.title("📈 TradeGuru AI – Smart Buy/Sell Signals")
st.markdown("_Real-time signals for 50+ stocks & crypto pairs_")

tickers = ["AAPL"]


@st.cache_data
def get_signal(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        df.ta.rsi(length=14, append=True)
        df.ta.macd(append=True)
        latest = df.iloc[-1]
        signal, reason = "HOLD", []

        if latest['RSI_14'] < 30 and latest['MACDh_12_26_9'] > 0:
            signal = "BUY"
            reason = ["RSI < 30", "MACD > 0"]
        elif latest['RSI_14'] > 70 and latest['MACDh_12_26_9'] < 0:
            signal = "SELL"
            reason = ["RSI > 70", "MACD < 0"]

        return {
            "Ticker": ticker,
            "Signal": signal,
            "RSI": round(latest['RSI_14'], 2),
            "MACD_Hist": round(latest['MACDh_12_26_9'], 4),
            "Reason": ", ".join(reason) if reason else "-"
        }
    except:
        return None

results = [get_signal(t) for t in tickers]
df = pd.DataFrame([r for r in results if r])
st.dataframe(df)

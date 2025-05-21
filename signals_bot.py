
import yfinance as yf
import pandas as pd
import pandas_ta as ta

tickers = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "NFLX", "AMD", "INTC",
    "BA", "BABA", "DIS", "UBER", "LYFT", "SHOP", "SQ", "PYPL", "PLTR", "SNOW",
    "CRM", "ORCL", "QCOM", "AVGO", "TXN", "MRNA", "JNJ", "PFE", "CVX", "XOM",
    "KO", "PEP", "MCD", "WMT", "HD", "COST", "TGT", "NKE", "SBUX", "WBA",
    "GS", "JPM", "BAC", "WFC", "V", "MA", "AXP", "T", "VZ", "TMUS",
    "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD"
]

def get_signals(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        df.ta.rsi(length=14, append=True)
        df.ta.macd(append=True)
        latest = df.iloc[-1]
        signal = "HOLD"
        reason = []

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

signals = [get_signals(t) for t in tickers]
df = pd.DataFrame([s for s in signals if s])
df.to_csv("tradeguru_signals.csv", index=False)
print(df)

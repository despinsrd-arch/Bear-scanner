import yfinance as yf
import pandas as pd

def fetch_yahoo(symbol):
    t = yf.Ticker(symbol)
    info = t.info

    price = info.get("currentPrice") or info.get("regularMarketPrice")
    roe = info.get("returnOnEquity")
    net_margin = info.get("netMargins")
    fcf = info.get("freeCashflow")
    pe = info.get("trailingPE")
    peg = info.get("pegRatio")
    ev_ebitda = info.get("enterpriseToEbitda")
    volume = info.get("volume")
    avg_volume = info.get("averageVolume")

    hist = t.history(period="6mo")
    ma50 = hist["Close"].rolling(50).mean().iloc[-1] if len(hist) >= 50 else None
    ma200 = hist["Close"].rolling(200).mean().iloc[-1] if len(hist) >= 200 else None

    return {
        "symbol": symbol,
        "price": price,
        "roe": roe,
        "net_margin": net_margin,
        "fcf": fcf,
        "pe": pe,
        "peg": peg,
        "ev_ebitda": ev_ebitda,
        "volume": volume,
        "avg_volume": avg_volume,
        "ma50": ma50,
        "ma200": ma200,
    }

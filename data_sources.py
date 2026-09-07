import yfinance as yf

def fetch_yahoo(symbol):
    try:
        t = yf.Ticker(symbol)
        info = t.info or {}

        # 1. Price & Liquidity
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        volume = info.get("volume") or info.get("regularMarketVolume")
        avg_volume = info.get("averageVolume") or info.get("averageDailyVolume3Month")

        # 2. Relative Volume (RVOL) - High volume surges
        rvol = (volume / avg_volume) if (volume and avg_volume and avg_volume > 0) else None

        # 3. Fast Moving Averages (directly from info API - zero extra network calls)
        ma50 = info.get("fiftyDayAverage")
        ma200 = info.get("twoHundredDayAverage")

        return {
            "symbol": symbol,
            "price": price,
            "roe": info.get("returnOnEquity"),
            "net_margin": info.get("profitMargins"),
            "fcf": info.get("freeCashflow"),
            "pe": info.get("trailingPE"),
            "peg": info.get("pegRatio"),
            "ev_ebitda": info.get("enterpriseToEbitda"),
            "volume": volume,
            "avg_volume": avg_volume,
            "rvol": round(rvol, 2) if rvol else None,
            "market_cap": info.get("marketCap"),
            "float": info.get("floatShares"),
            "short_ratio": info.get("shortRatio"),
            "ma50": ma50,
            "ma200": ma200,
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
        }
    except Exception:
        return None

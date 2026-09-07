import asyncio
from async_fetch import fetch_batch
from scoring import score_stock
from universe import load_tickers


def build_metrics(symbol, quote):
    """Extract metrics from Yahoo JSON quote with bulletproof price resolution."""

    # Search all possible price locations in Yahoo JSON payload
    price = (
        quote.get("regularMarketPrice")
        or quote.get("currentPrice")
        or quote.get("postMarketPrice")
        or quote.get("preMarketPrice")
        or quote.get("previousClose")
        or quote.get("ask")
        or quote.get("bid")
    )

    volume = quote.get("regularMarketVolume") or quote.get("volume") or 0
    avg_vol = quote.get("averageDailyVolume3Month") or quote.get("averageVolume") or 1

    # Compute Relative Volume (RVOL)
    rvol = (volume / avg_vol) if (avg_vol > 0) else None

    metrics = {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "avg_volume": avg_vol,
        "rvol": round(rvol, 2) if rvol else None,
        "pe": quote.get("trailingPE"),
        "peg": quote.get("pegRatio"),
        "roe": quote.get("returnOnEquity"),
        "net_margin": quote.get("profitMargins"),
        "fcf": quote.get("freeCashflow"),
        "market_cap": quote.get("marketCap"),
        "float": quote.get("floatShares"),
        "short_ratio": quote.get("shortRatio"),
        "ma50": quote.get("fiftyDayAverage"),
        "ma200": quote.get("twoHundredDayAverage"),
        "52w_high": quote.get("fiftyTwoWeekHigh"),
        "52w_low": quote.get("fiftyTwoWeekLow"),
    }

    # Compute EV/EBITDA safely
    ev = quote.get("enterpriseValue")
    ebitda = quote.get("ebitda")

    if ev and ebitda:
        try:
            metrics["ev_ebitda"] = ev / ebitda
        except Exception:
            metrics["ev_ebitda"] = None
    else:
        metrics["ev_ebitda"] = None

    return metrics


def run_screen(tickers=None):
    """Fetch tickers async, filter by price ($0.001 - $35), score them, and return top 20 matches."""

    # 1. Load ticker universe
    universe = tickers if tickers is not None else load_tickers()
    print(f"DEBUG: Loaded {len(universe)} tickers from universe.")

    # 2. Async fetch all Yahoo JSON quotes concurrently (~10-15 seconds)
    results = asyncio.run(fetch_batch(universe))
    print(f"DEBUG: Fetched {len(results)} results from Yahoo.")

    scored = []

    # 3. Filter and score stocks
    for symbol, quote in results:
        if not quote:
            continue

        metrics = build_metrics(symbol, quote)
        price = metrics.get("price")

        # PRICE FILTER: Only allow stocks between $0.001 and $35.00
        if price is None or not (0.001 <= price <= 35.0):
            continue

        try:
            score = score_stock(metrics)
            if score is None:
                score = 0.0
            metrics["score"] = round(score, 2)
            scored.append(metrics)
        except Exception:
            metrics["score"] = 0.0
            scored.append(metrics)

    print(f"DEBUG: Scored {len(scored)} stocks within price range.")

    # 4. Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    # 5. Return top 20 matches
    return scored[:20]

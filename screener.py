import asyncio
from async_fetch import fetch_batch
from scoring import score_stock
from universe import load_tickers


def build_metrics(symbol, quote):
    """Extract metrics from Yahoo JSON quote with price fallback logic."""

    # Price fallback logic for market off-hours/pre-market
    price = (
        quote.get("regularMarketPrice")
        or quote.get("currentPrice")
        or quote.get("postMarketPrice")
        or quote.get("previousClose")
    )

    volume = quote.get("regularMarketVolume") or quote.get("volume")
    avg_vol = quote.get("averageDailyVolume3Month") or quote.get("averageVolume")

    # Compute Relative Volume (RVOL)
    rvol = (volume / avg_vol) if (volume and avg_vol and avg_vol > 0) else None

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

    universe = tickers if tickers is not None else load_tickers()

    # Async fetch all Yahoo JSON quotes concurrently (~10-15 seconds)
    results = asyncio.run(fetch_batch(universe))

    scored = []

    for symbol, quote in results:
        if not quote:
            continue

        metrics = build_metrics(symbol, quote)
        price = metrics.get("price")

        # ----------------------------------------------------
        # PRICE FILTER: Strictly enforce $0.001 to $35.00
        # ----------------------------------------------------
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

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    # Return top 20 matches
    return scored[:20]

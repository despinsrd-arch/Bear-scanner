import asyncio
from async_fetch import fetch_batch
from scoring import score_stock
from universe import load_tickers


def build_metrics(symbol, quote):
    """Extract metrics from Yahoo JSON quote and compute EV/EBITDA."""

    metrics = {
        "symbol": symbol,
        "price": quote.get("regularMarketPrice"),
        "volume": quote.get("regularMarketVolume"),
        "avg_volume": quote.get("averageDailyVolume3Month"),
        "pe": quote.get("trailingPE"),
        "peg": quote.get("pegRatio"),
        "ma50": quote.get("fiftyDayAverage"),
        "ma200": quote.get("twoHundredDayAverage"),
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
    """Fetch tickers async, filter by price ($0.001 - $35), score them, and return top matches."""

    # Use passed tickers or fallback to loading full universe
    universe = tickers if tickers is not None else load_tickers()

    # Async fetch all Yahoo JSON quotes
    results = asyncio.run(fetch_batch(universe))

    scored = []

    for symbol, quote in results:
        if not quote:
            continue

        metrics = build_metrics(symbol, quote)
        price = metrics.get("price")

        # ----------------------------------------------------
        # PRICE FILTER: Only allow stocks between $0.001 and $35.00
        # ----------------------------------------------------
        if price is None or not (0.001 <= price <= 35.0):
            continue

        try:
            score = score_stock(metrics)
            if score is not None:
                metrics["score"] = round(score, 2)
                scored.append(metrics)
        except Exception:
            continue

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    # Return top 20 matches in price range
    return scored[:20]

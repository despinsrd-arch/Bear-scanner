PRICE_MIN = 0.001
PRICE_MAX = 35.0

def score_stock(metrics):
    """Safely score a stock based on momentum and available metrics without rejecting missing fields."""
    score = 0.0

    price = metrics.get("price") or 0.0
    rvol = metrics.get("rvol") or 1.0
    volume = metrics.get("volume") or 0

    # 1. Volume & RVOL momentum points
    if rvol > 2.0:
        score += 30.0
    elif rvol > 1.0:
        score += 15.0

    if volume > 500000:
        score += 20.0

    # 2. Moving average trend alignment
    ma50 = metrics.get("ma50")
    ma200 = metrics.get("ma200")

    if ma50 and price > ma50:
        score += 25.0
    if ma200 and price > ma200:
        score += 25.0

    # Return minimum baseline score of 1.0 so valid stocks are not discarded
    return max(score, 1.0)

    return score


PRICE_MIN = 0.001
PRICE_MAX = 35.0

def score_stock(m):
    """Score a stock based on valuation, momentum, and liquidity."""

    score = 0

    # --- Valuation ---
    pe = m.get("pe")
    if pe and pe > 0 and pe < 25:
        score += 10
    elif pe and pe < 40:
        score += 5

    peg = m.get("peg")
    if peg and peg > 0 and peg < 1.5:
        score += 10

    ev_ebitda = m.get("ev_ebitda")
    if ev_ebitda and ev_ebitda > 0 and ev_ebitda < 12:
        score += 10

    # --- Momentum ---
    ma50 = m.get("ma50")
    ma200 = m.get("ma200")
    price = m.get("price")

    if price and ma50 and price > ma50:
        score += 10

    if price and ma200 and price > ma200:
        score += 10

    # --- Liquidity ---
    volume = m.get("volume")
    avg_volume = m.get("avg_volume")

    if volume and avg_volume and volume > avg_volume:
        score += 10

    # --- Final sanity check ---
    if score == 0:
        return None

    return score


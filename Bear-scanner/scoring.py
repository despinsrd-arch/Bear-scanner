PRICE_MIN = 0.001
PRICE_MAX = 35.0

def score_stock(m):
    if m["price"] is None or not (PRICE_MIN <= m["price"] <= PRICE_MAX):
        return None

    score = 0.0

    if m["roe"]:
        score += float(m["roe"]) * 50
    if m["net_margin"]:
        score += float(m["net_margin"]) * 100

    if m["pe"]:
        score += max(0, 40 - float(m["pe"]))
    if m["peg"]:
        score += max(0, 30 - float(m["peg"]))
    if m["ev_ebitda"]:
        score += max(0, 25 - float(m["ev_ebitda"]))

    if m["volume"] and m["avg_volume"] and m["avg_volume"] > 0:
        score += (m["volume"] / m["avg_volume"]) * 10

    if m["ma50"] and m["price"] > m["ma50"]:
        score += 10
    if m["ma200"] and m["price"] > m["ma200"]:
        score += 10

    return score

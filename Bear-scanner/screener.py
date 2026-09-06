import csv
from data_sources import fetch_yahoo
from scoring import score_stock

def load_tickers():
    tickers = []
    with open("tickers.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            tickers.append(row[0].strip())
    return tickers

def run_screen():
    universe = load_tickers()
    scored = []

    for symbol in universe:
        try:
            metrics = fetch_yahoo(symbol)
            s = score_stock(metrics)
            if s is not None:
                metrics["score"] = round(s, 2)
                scored.append(metrics)
        except Exception as e:
            print(f"Error on {symbol}: {e}")

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:20]

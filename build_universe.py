import csv
import yfinance as yf

# A starter list of US + Canadian tickers.
# We will expand this list later.
US_CA_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "NVDA", "META", "AMD", "NFLX", "INTC",
    "ENB.TO", "SHOP.TO", "TD.TO", "RY.TO", "BMO.TO",
    "BNS.TO", "CNQ.TO", "SU.TO", "CP.TO", "CNR.TO"
]

def filter_by_price(tickers):
    final = []
    for symbol in tickers:
        try:
            t = yf.Ticker(symbol)
            info = t.info
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            if price and 0.001 <= price <= 35:
                final.append(symbol)
        except:
            pass
    return final

def build_universe():
    print("Filtering tickers by price...")
    filtered = filter_by_price(US_CA_TICKERS)
    print(f"Tickers after price filter: {len(filtered)}")

    with open("tickers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for symbol in filtered:
            writer.writerow([symbol])

    print("Done! tickers.csv updated.")

if __name__ == "__main__":
    build_universe()

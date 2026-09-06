import csv
import yfinance as yf

def load_full_universe(path="full_tickers_clean.csv"):
    tickers = []
    with open(path, "r") as f:
        for row in f:
            t = row.strip()
            if t:
                tickers.append(t)
    return tickers

def main():
    full = load_full_universe()
    print(f"Loaded {len(full)} tickers from full_tickers_clean.csv")

    filtered = []

    for t in full:
        try:
            data = yf.Ticker(t)
            hist = data.history(period="3mo")

            # Keep anything with ANY real price history
            if hist is None or hist.empty:
                continue

            last_close = hist["Close"].iloc[-1]

            # Allow anything above $0.50
            if last_close is None or last_close < 0.50:
                continue

            filtered.append(t)

        except Exception:
            continue

    print(f"Filtered universe size: {len(filtered)}")

    with open("tickers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for t in filtered:
            writer.writerow([t])

    print("tickers.csv updated with expanded universe.")

if __name__ == "__main__":
    main()


import csv
import yfinance as yf

def load_tickers(path="tickers.csv"):
    tickers = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                tickers.append(row[0].strip())
    return tickers

def fetch_data(ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="6mo")

        if hist is None or hist.empty:
            print(f"{ticker}: no price data found (skipped)")
            return None

        hist = hist.dropna()
        if hist.empty:
            print(f"{ticker}: all price data was NaN (skipped)")
            return None

        last_close = hist["Close"].iloc[-1]

        if last_close is None or last_close <= 0:
            print(f"{ticker}: invalid last close (skipped)")
            return None

        # Timeframe closes
        close_1w = hist["Close"].iloc[-5] if len(hist) >= 5 else None
        close_1m = hist["Close"].iloc[-22] if len(hist) >= 22 else None
        close_3m = hist["Close"].iloc[-66] if len(hist) >= 66 else None
        close_6m = hist["Close"].iloc[0]

        def pct(a, b):
            try:
                return ((a - b) / b * 100) if (a is not None and b is not None) else None
            except Exception:
                return None

        return {
            "ticker": ticker,
            "last_close": last_close,
            "change_1w": pct(last_close, close_1w),
            "change_1m": pct(last_close, close_1m),
            "change_3m": pct(last_close, close_3m),
            "change_6m": pct(last_close, close_6m),
        }

    except Exception as e:
        print(f"{ticker}: fatal error ({e}) — skipped")
        return None

import csv

def save_results(all_results, winners):
    # Save full results
    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Last Close", "1W %", "1M %", "3M %", "6M %"])
        for r in all_results:
            writer.writerow([
                r["ticker"],
                r["last_close"],
                r["change_1w"],
                r["change_1m"],
                r["change_3m"],
                r["change_6m"]
            ])

    # Save winners only
    with open("winners.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "3M %", "1M %", "1W %", "6M %"])
        for r in winners:
            writer.writerow([
                r["ticker"],
                r["change_3m"],
                r["change_1m"],
                r["change_1w"],
                r["change_6m"]
            ])

    print("results.csv and winners.csv saved.")


def main():
    tickers = load_tickers()
    print(f"Loaded {len(tickers)} tickers from tickers.csv")

    results = []
    for i, t in enumerate(tickers, start=1):
        try:
            print(f"Processing {i}/{len(tickers)}: {t}")
            info = fetch_data(t)
            if info is not None:
                if info["last_close"] < 1:
                    continue
                results.append(info)
        except Exception as e:
            print(f"{t}: fatal loop error ({e}) — skipped")
            continue

    winners = [
        r for r in results
        if r["change_3m"] is not None and r["change_3m"] > 20
    ]
    winners.sort(key=lambda x: x["change_3m"], reverse=True)

    print("\nTop momentum tickers (3-month change > 20%):\n")

    for r in winners[:50]:
        print(
            f"{r['ticker']:8}  "
            f"1W: {r['change_1w']:6.2f}%  "
            f"1M: {r['change_1m']:6.2f}%  "
            f"3M: {r['change_3m']:6.2f}%  "
            f"6M: {r['change_6m']:6.2f}%"
        )

    save_results(results, winners)


if __name__ == "__main__":
    main()
from fastapi import FastAPI
from fastapi.responses import JSONResponse

api = FastAPI()

@api.get("/")
def home():
    return {"message": "HardHatHQ Scanner is running"}

@api.get("/screen")
def run_scan():
    tickers = load_tickers()
    results = []

    for t in tickers:
        info = fetch_data(t)
        if info is not None:
            results.append(info)

    winners = [
        r for r in results
        if r["change_3m"] is not None and r["change_3m"] > 20
    ]

    winners.sort(key=lambda x: x["change_3m"], reverse=True)

    return JSONResponse(content=winners)


if __name__ == "__main__":
    main()

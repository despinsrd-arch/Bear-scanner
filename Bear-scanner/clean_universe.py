import csv

clean = []

with open("full_tickers.csv", "r", encoding="utf-8") as f:
    for line in f:
        t = line.strip().upper()          # remove spaces + uppercase
        t = t.split(",")[0]               # remove extra columns
        t = t.replace("\t", "")           # remove tabs
        t = t.replace("\r", "")           # remove carriage returns

        # skip empty lines
        if not t:
            continue

        # skip anything not A–Z or numbers
        if not t.replace("-", "").isalnum():
            continue

        # skip crypto tokens just in case
        if t.endswith("USD") or t.endswith("USDT") or t.endswith("USDC"):
            continue

        clean.append(t)

# remove duplicates
clean = sorted(list(set(clean)))

# save cleaned file
with open("full_tickers_clean.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for t in clean:
        writer.writerow([t])

print(f"Cleaned tickers: {len(clean)}")
print("Saved to full_tickers_clean.csv")

import csv
import os

def load_tickers():
    tickers = []
    # Path to your cleaned CSV file
    csv_path = os.path.join(os.path.dirname(__file__), "full_tickers_clean.csv")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    tickers.append(row[0])
        return tickers
    
    # Fallback default universe if CSV is missing
    return ["SOUN", "LENZ", "AHCO", "EGY", "EVLV", "KOPN", "LTRX", "PXLW"]
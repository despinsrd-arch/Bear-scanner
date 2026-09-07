import os
import pandas as pd

def load_tickers():
    """Load ticker list safely from CSV, falling back to a default list if missing."""
    # Find the current directory of this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "full_tickers_clean.csv")

    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            # Find the symbol column (handles 'symbol', 'Symbol', or first column)
            col = "symbol" if "symbol" in df.columns else ("Symbol" if "Symbol" in df.columns else df.columns[0])
            tickers = df[col].dropna().astype(str).str.strip().tolist()
            if tickers:
                return tickers
        except Exception as e:
            print(f"Error loading CSV: {e}")

    # Fallback list if CSV isn't found on Render
    print("WARNING: full_tickers_clean.csv not found! Using fallback ticker list.")
    return ["SOUN", "LENZ", "AHCO", "EGY", "EVLV", "KOPN", "LTRX", "PXLW", "AAPL", "AMD", "PLTR", "SOFI"]

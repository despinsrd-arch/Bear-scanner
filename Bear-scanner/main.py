from fastapi import FastAPI
from screener import run_screen
from universe import load_tickers

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Advanced Screener Running"}

@app.get("/screen")
async def screen():
    # 1. Load the full ticker universe (2,766 tickers from CSV)
    tickers = load_tickers()
    
    # 2. Run the screen on the loaded universe
    results = await run_screen(tickers)
    
    # 3. Return the total scanned count, matches found, and stock results
    return {
        "status": "success",
        "scanned_count": len(tickers),
        "matches_found": len(results),
        "stocks": results
    }

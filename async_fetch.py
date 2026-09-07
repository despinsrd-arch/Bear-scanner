import asyncio
import aiohttp

# Controlled concurrency to prevent Render IP blocks
MAX_CONCURRENT_REQUESTS = 25

async def fetch_quote(session, semaphore, symbol):
    """Fetch raw price and volume directly from Yahoo Finance Chart API."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    async with semaphore:
        try:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=6)) as response:
                if response.status == 200:
                    data = await response.json()
                    chart = data.get("chart", {}).get("result", [])
                    if chart and len(chart) > 0:
                        meta = chart[0].get("meta", {})
                        
                        # Extract price fallbacks directly from Yahoo chart meta
                        price = (
                            meta.get("regularMarketPrice")
                            or meta.get("chartPreviousClose")
                            or meta.get("previousClose")
                        )
                        
                        volume = meta.get("regularMarketVolume") or 0
                        avg_vol = meta.get("averageDailyVolume3Month") or 1
                        
                        return symbol, {
                            "regularMarketPrice": price,
                            "regularMarketVolume": volume,
                            "averageDailyVolume3Month": avg_vol,
                            "trailingPE": meta.get("trailingPE"),
                            "fiftyDayAverage": meta.get("fiftyDayAverage"),
                            "twoHundredDayAverage": meta.get("twoHundredDayAverage"),
                            "fiftyTwoWeekHigh": meta.get("fiftyTwoWeekHigh"),
                            "fiftyTwoWeekLow": meta.get("fiftyTwoWeekLow")
                        }
                return symbol, None
        except Exception:
            return symbol, None


async def fetch_batch(symbols):
    """Fetch quotes for all tickers concurrently."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_quote(session, semaphore, s) for s in symbols]
        results = await asyncio.gather(*tasks)
        return results

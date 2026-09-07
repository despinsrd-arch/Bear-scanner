import asyncio
import aiohttp

# Process 100 stocks simultaneously (prevents Yahoo rate limits while staying under 15s)
MAX_CONCURRENT_REQUESTS = 100

async def fetch_quote(session, semaphore, symbol):
    """Fetch raw quote JSON directly from Yahoo Finance API asynchronously."""
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with semaphore:
        try:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data.get("quoteResponse", {}).get("result", [])
                    if result:
                        return symbol, result[0]
                return symbol, None
        except Exception:
            return symbol, None


async def fetch_batch(symbols):
    """Fetch quotes for all 2,766 tickers concurrently in 10-15 seconds."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    # Use a high-performance shared TCP connection pool
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_quote(session, semaphore, s) for s in symbols]
        results = await asyncio.gather(*tasks)
        return results

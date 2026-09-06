import aiohttp
import asyncio
import yfinance as yf

async def fetch_one(session, symbol):
    try:
        data = yf.Ticker(symbol).info
        return symbol, data
    except Exception:
        return symbol, None

async def fetch_batch(symbols):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, s) for s in symbols]
        return await asyncio.gather(*tasks)

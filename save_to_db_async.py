import asyncio
import aiohttp
import pandas as pd

tickers = ["AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "NVDA", "META"]

async def fetch_price(session, ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=7d&interval=1d"
    async with session.get(url) as response:
        data = await response.json()
        try:
            timestamp = data['chart']['result'][0]['timestamp']
            close = data['chart']['result'][0]['indicators']['quote'][0]['close']
            return pd.DataFrame({"Date": pd.to_datetime(timestamp, unit="s"), "Close": close, "Ticker": ticker})
        except Exception as e:
            print(f"{ticker} 실패: {e}")
            return None

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price(session, ticker) for ticker in tickers]
        results = await asyncio.gather(*tasks)

    df_all = pd.concat([df for df in results if df is not None], ignore_index=True)
    df_all.to_csv("async_stocks.csv", index=False)
    print("모든 종목 비동기 저장 완료")

asyncio.run(main())

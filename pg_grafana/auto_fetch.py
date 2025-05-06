# auto_fetch.py

from sqlalchemy import create_engine
import yfinance as yf
import pandas as pd
from datetime import datetime

# PostgreSQL 연결
engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres")

# 종목 리스트
TICKERS = [
    "AAPL", "TSLA", "MSFT", "GOOG", "AMZN",
    "META", "NVDA", "NFLX", "INTC", "AMD",
    "JPM", "BAC", "WFC", "GS",
    "XOM", "CVX", "BP",
    "KO", "PEP", "PG", "JNJ",
    "SPY", "QQQ", "DIA", "ARKK"
]

# 오늘 날짜 기준 1일치 데이터만 수집
today = datetime.today().strftime('%Y-%m-%d')
print(f"[{today}] 주가 수집 시작")

for ticker in TICKERS:
    try:
        df = yf.download(ticker, period="7d", interval="1d", auto_adjust=False)
        df = df.reset_index()
        df.rename(columns={"Adj Close": "adj_close", "Date": "date"}, inplace=True)
        df["ticker"] = ticker.lower()
        df.to_sql("stocks", engine, if_exists="append", index=False)
        print(f"{ticker} 저장 완료 ✅")
    except Exception as e:
        print(f"{ticker} 저장 실패 ❌: {e}")

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 종목 리스트 (원하는 만큼 추가 가능)
tickers = ["AAPL", "GOOG", "TSLA", "MSFT", "AMZN"]

# 날짜 자동 설정: 오늘 기준 최근 3년
end_date = datetime.today()
start_date = end_date - timedelta(days = 3 * 365)

# 각 종목에 대해 데이터 다운로드 및 저장
for ticker in tickers:
    print(f"Downloading {ticker} data ...")
    df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
    if not df.empty:
        df.to_csv(f"{ticker}.csv")
        print(f"{ticker}.csv 저장 완료")
    else:
        print(f"{ticker} 데이터 없음 (패스)")
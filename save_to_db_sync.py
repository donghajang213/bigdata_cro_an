from sqlalchemy import create_engine, text
import pandas as pd
import yfinance as yf

# 1. PostgreSQL 연결
engine = create_engine("postgresql://postgres:1234@localhost:5433/postgres")

# 2. 테이블 재생성 (컬럼은 모두 소문자!)
with engine.begin() as conn:
    conn.execute(text("""
        DROP TABLE IF EXISTS stocks;
        CREATE TABLE stocks (
            date DATE,
            close FLOAT,
            adj_close FLOAT,
            high FLOAT,
            low FLOAT,
            open FLOAT,
            volume BIGINT,
            ticker VARCHAR(10),
            CONSTRAINT unique_date_ticker UNIQUE (date, ticker)
        );
    """))
    print("✅ stocks 테이블이 소문자 컬럼으로 재생성되었습니다.")


# csv 파일 저장
# csv_files = glob.glob("./csv/*.csv")
# for file in csv_files:
#     ticker = os.path.basename(file).replace(".csv", "")
#     df = pd.read_csv(file)
#     df["Ticker"] = ticker                     # ❗ 기존 컬럼명 (대문자)
#     df.to_sql("stocks", con=engine, if_exists="append", index=False)
#     print(f"{ticker} CSV → DB 저장 완료")

# 종목 수집
TICKERS = [
    "AAPL", "TSLA", "MSFT", "GOOG", "AMZN",  # 기존
    "META", "NVDA", "NFLX", "INTC", "AMD",   # 반도체 & 빅테크
    "JPM", "BAC", "WFC", "GS",               # 금융
    "XOM", "CVX", "BP",                      # 에너지
    "KO", "PEP", "PG", "JNJ",                # 소비재/헬스케어
    "SPY", "QQQ", "DIA", "ARKK"              # ETF
]

# 3. 동기식으로 Yahoo Finance에서 수집 → DB 저장
for ticker in TICKERS:
    try:
        df = yf.download(ticker, period="7d", interval="1d", auto_adjust=False)
        df = df.reset_index()

        # 컬럼 이름 정리 (MultiIndex 방지)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # 컬럼명 수정 (모두 소문자 통일)
        df.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume"
        }, inplace=True)

        df["ticker"] = ticker  # 소문자 컬럼명으로 통일

        # 저장
        df.to_sql("stocks", con=engine, if_exists="append", index=False)
        print(f"{ticker} 저장 완료 ✅")

    except Exception as e:
        print(f"{ticker} 저장 중 오류 발생 ❌: {e}")

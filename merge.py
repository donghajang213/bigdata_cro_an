import pandas as pd
import glob
import os

csv_files = glob.glob("./csv/*.csv")
all_data = []

# 실제 우리가 원하는 컬럼 순서
columns = ["Date", "Close", "High", "Low", "Open", "Volume"]

for file in csv_files:
    ticker = os.path.basename(file).replace(".csv", "")

    try:
        # 헤더 없이 4번째 줄부터 데이터로 읽음
        df = pd.read_csv(file, header=None, skiprows=3, names=columns)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Ticker"] = ticker
        all_data.append(df)
    except Exception as e:
        print(f"{file} 오류 발생: {e}")

merged_df = pd.concat(all_data, ignore_index=True)
merged_df.to_csv("merged_stocks.csv", index=False)
print("병합 완료 → merged_stocks.csv 저장됨")

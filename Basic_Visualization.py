import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc # 한국어 깨짐 해결
import os

# 한글 폰트 설정
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf") 
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False


df = pd.read_csv("./csv/merged_stocks.csv")

# 날짜를 datetime 형식으로 변환
df["Date"] = pd.to_datetime(df["Date"])

# 종목별 종가 그래프
plt.figure(figsize=(14, 7))

for ticker in df["Ticker"].unique():
    sub_df = df[df["Ticker"] == ticker]
    plt.plot(sub_df["Date"], sub_df["Close"], label = ticker)

plt.title("미국 주식 종가 변화 (최근 3년)", fontsize = 16)
plt.xlabel("날짜")
plt.ylabel("종가")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
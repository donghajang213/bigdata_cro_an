import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# 한글 폰트 설정 (상대 경로)
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf") 
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = pd.read_csv("./csv/merged_stocks.csv")
df["Date"] = pd.to_datetime(df["Date"])

# 시각화할 종목 선택 (예: AAPL)
target = "AAPL"
sub_df = df[df["Ticker"] == target].sort_values("Date")

# 이동 평균선 계산
sub_df["MA20"] = sub_df["Close"].rolling(window=20).mean()
sub_df["MA60"] = sub_df["Close"].rolling(window=60).mean()

# 그래프 그리기
fig, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1, sharex = True, figsize = (14, 9), gridspec_kw={"height_ratios": [3, 1]})

ax1.plot(sub_df["Date"], sub_df["Close"], label="종가", color="blue")
ax1.plot(sub_df["Date"], sub_df["MA20"], label="20일선", linestyle="--", color = "green")
ax1.plot(sub_df["Date"], sub_df["MA60"], label="60일선", linestyle="--", color = "red")
ax1.set_title(f"{target} 주가 및 이동 평균선", fontsize=16)
ax1.set_ylabel("종가 (USD)")
ax1.legend()
ax1.grid(True)

# 최고가 위치
max_idx = sub_df["Close"].idxmax()
max_date = sub_df.loc[max_idx, "Date"]
max_price = sub_df.loc[max_idx, "Close"]

# 최저가 위치
min_idx = sub_df["Close"].idxmin()
min_date = sub_df.loc[min_idx, "Date"]
min_price = sub_df.loc[min_idx, "Close"]

# ax1에 마커 추가
ax1.scatter(max_date, max_price, color="red", label="최고가", zorder=5)
ax1.annotate(f"최고가 {max_price:.2f}", xy=(max_date, max_price),
             xytext=(max_date, max_price + 10),
             arrowprops=dict(arrowstyle="->", color="red"),
             fontsize=10, color="red")

ax1.scatter(min_date, min_price, color="blue", label="최저가", zorder=5)
ax1.annotate(f"최저가 {min_price:.2f}", xy=(min_date, min_price),
             xytext=(min_date, min_price - 10),
             arrowprops=dict(arrowstyle="->", color="blue"),
             fontsize=10, color="blue")


# 거래량 (막대 그래프)
ax2.bar(sub_df["Date"], sub_df["Volume"], label = "거래량", color = "gray", width = 1.0)
ax2.set_ylabel("거래량")
ax2.set_xlabel("날짜")
ax2.grid(True)

plt.tight_layout()
plt.show()
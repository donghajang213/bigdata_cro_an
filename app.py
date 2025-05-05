import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 폰트 설정 (한글용)
from matplotlib import font_manager
import os
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = pd.read_csv("./csv/merged_stocks.csv")
df["Date"] = pd.to_datetime(df["Date"])

# 제목
st.title("📈 미국 주식 시각화 대시보드")

# 종목 선택
tickers = df["Ticker"].unique().tolist()
selected = st.selectbox("종목을 선택하세요", tickers)

# 해당 종목 필터링
sub_df = df[df["Ticker"] == selected].sort_values("Date")
sub_df["MA20"] = sub_df["Close"].rolling(window=20).mean()
sub_df["MA60"] = sub_df["Close"].rolling(window=60).mean()

# 최고/최저가 찾기
max_idx = sub_df["Close"].idxmax()
min_idx = sub_df["Close"].idxmin()
max_date, max_price = sub_df.loc[max_idx, ["Date", "Close"]]
min_date, min_price = sub_df.loc[min_idx, ["Date", "Close"]]

# 그래프
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(12, 8), gridspec_kw={"height_ratios": [3, 1]})

# 종가 + MA
ax1.plot(sub_df["Date"], sub_df["Close"], label="종가", color="blue")
ax1.plot(sub_df["Date"], sub_df["MA20"], label="20일선", linestyle="--", color="green")
ax1.plot(sub_df["Date"], sub_df["MA60"], label="60일선", linestyle="--", color="red")
ax1.scatter(max_date, max_price, color="red", label="최고가", zorder=5)
ax1.scatter(min_date, min_price, color="blue", label="최저가", zorder=5)
ax1.legend()
ax1.set_title(f"{selected} 주가 및 이동 평균선")
ax1.grid(True)

# 거래량
ax2.bar(sub_df["Date"], sub_df["Volume"], color="gray", width=1.0)
ax2.set_ylabel("거래량")
ax2.set_xlabel("날짜")
ax2.grid(True)

st.pyplot(fig)

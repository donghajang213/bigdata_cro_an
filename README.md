# bigdata_cro_an
빅데이터 크롤링, 분석

## API 활용 방식 (권장)

추천 API

1. Yahoo Finance (yfinance) - 무료
pip install yfinance

## 웹 대시보드 만들기
pip install streamlit
pip install altair==4.2.2

## Docker 실행 후(로컬)
docker run --name pgstock -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres

## PostgreSQL 패키지 설치
pip install sqlalchemy psycopg2-binary yfinance pandas

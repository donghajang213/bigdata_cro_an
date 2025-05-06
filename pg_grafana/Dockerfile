FROM python:3.9-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y cron && pip install --no-cache-dir yfinance sqlalchemy psycopg2-binary pandas

# 작업 디렉토리
WORKDIR /app

# 소스 코드 복사
COPY auto_fetch.py .
COPY crontab.txt .

# 크론탭 등록
RUN crontab crontab.txt

# 로그 파일 위치
RUN touch /var/log/cron.log

# cron 실행
CMD cron && tail -f /var/log/cron.log

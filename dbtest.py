# from sqlalchemy import create_engine
# import pandas as pd

# # PostgreSQL 연결 (DB 정보는 자신의 환경에 맞게 조정)
# engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres")

# # stocks 테이블에서 최근 10개 데이터 확인
# with engine.connect() as conn:
#     df = pd.read_sql("""
#         SELECT *
#         FROM stocks
#         ORDER BY date DESC
#         LIMIT 10;
#     """, conn)
#     print(df)

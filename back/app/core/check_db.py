import sqlite3
import os

# 현재 파일(back/app/core) 기준으로 프로젝트 루트 경로 계산
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
db_path = os.path.join(BASE_DIR, "blog.db")

print("📌 Checking DB at:", db_path)

# with 구문으로 안전하게 연결
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # 모든 테이블 이름 조회
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        print("⚠️ No tables found in the DB!")
    else:
        print("📌 Tables in blog.db:")
        for table in tables:
            print(" -", table[0])

    # 모든 테이블 컬럼 정보 확인
    for table in tables:
        table_name = table[0]
        print(f"\n📌 Columns in table '{table_name}':")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            # col tuple 구조: (cid, name, type, notnull, dflt_value, pk)
            cid, name, col_type, notnull, dflt, pk = col
            print(f" - {name} ({col_type}){' NOT NULL' if notnull else ''}{' PRIMARY KEY' if pk else ''}")

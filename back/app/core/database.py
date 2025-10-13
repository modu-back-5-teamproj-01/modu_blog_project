import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey # ForeignKey 추가
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# 모델 import

from app.models import comment, post_tag, post, session, tag, upload, user   # 모델들 반드시 import
from app.models.base import Base
# from ..models.base import Base

# .env 파일 로드
load_dotenv()
# 데이터베이스 연결 URL 설정
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

# engine과 Base 정의

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()



# 테이블 생성 (engine과 Base가 정의된 후 실행)
Base.metadata.create_all(bind=engine)

# app/core/database.py에 추가
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey # ForeignKey 추가
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..models.base import Base

# 데이터베이스 연결 URL 설정
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

# engine과 Base 정의
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# User 클래스 정의
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)

# Post 클래스 정의
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id")) # 사용자 연결
    created_at = Column(DateTime, default=datetime.datetime.now)

# 테이블 생성 (engine과 Base가 정의된 후 실행)
Base.metadata.create_all(bind=engine)
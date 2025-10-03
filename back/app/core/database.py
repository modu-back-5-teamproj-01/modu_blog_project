from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# SQLALCHEMY_DATABASE_URL = ""
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     created_at = Column(DateTime, default=datetime.datetime.now)


# class Post(Base):
#     __tablename__ = "posts"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     cintent = Column(String)
#     # user_id= Column(Integer, ForeignKey("users.id")) # 사용자 연결
#     created_at = Column(DateTime, default=datetime.datetime.now)


# # 테이블 생성
# Base.metadata.create_all(bind=engine)


# 다음은 프로젝트 초기용 코드입니다!
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
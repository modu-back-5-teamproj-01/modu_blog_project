from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

# DB 파일 경로 설정 (경로 확인 필수)
# 현재 프로젝트 구조 기준으로 상대 경로를 사용합니다.
SQLALCHEMY_DATABASE_URL = "sqlite:///./back/app/data/blog.db" 

# DB 연결 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Base 객체 정의 (모든 모델이 상속받습니다)
Base = declarative_base() 

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 세션을 제공하는 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from fastapi import FastAPI

# 🚨 1. 라우터 임포트 수정: ai 모듈 추가
import back.app.routers.auth as auth
import back.app.routers.user as user
import back.app.routers.post as post
import back.app.routers.ai as ai  # <--- 이 줄 추가

# 코어 파일 임포트
from back.app.core.database import Base, engine 

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🚨 2. 라우터 등록 수정: ai 라우터 등록 추가
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(ai.router, prefix="/ai", tags=["ai"]) # <--- 이 줄 추가

@app.get("/")
def read_root():
    return {"message": "Welcome to Modu Blog API"}
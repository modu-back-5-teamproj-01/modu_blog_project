# back/app/main.py 파일 전체 내용 (상대 경로 임포트로 변경)

from fastapi import FastAPI
# 🚨 라우터 임포트 수정 (main.py가 있는 위치에서 상대적으로 임포트)
from .routers import auth, user, post # routers/__init__.py에 의존하지 않고 바로 모듈을 찾습니다.

from .core.database import Base, engine 

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 등록
# 라우터 파일의 router 객체 사용 시, 'user.router'와 같이 사용하려면
# from .routers import user 와 같이 임포트하는 것이 더 자연스럽습니다.
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Modu Blog API"}
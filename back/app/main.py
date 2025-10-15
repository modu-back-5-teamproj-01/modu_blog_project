from fastapi import FastAPI, Request
from app.routers import auth, blog, comment
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, Response
import os
from fastapi.middleware.cors import CORSMiddleware
# from routers import auth, posts

app = FastAPI()

# ✅ front 정적 파일 연결
FRONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "front")
# 경로 확인용 출력
print("Static path: ", FRONT_DIR)
# CSS, JS, 이미지 등 정적 파일 서빙
app.mount("/static", StaticFiles(directory=FRONT_DIR), name="static")


# app.include_router(auth.router, prefix="/api")
# app.include_router(posts.router, prefix="/api")
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(comment.router)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ "/" 경로 접근 시 index.html 반환
@app.get("/")
async def serve_index():
    return RedirectResponse(url="/static/index.html")
    return 
    # index_path = os.path.join(FRONT_DIR, "index.html")
    # return FileResponse(index_path)

@app.middleware("http")
async def ignore_wellknown_requests(request: Request, call_next):
    if request.url.path.startswith("/.well-known"):
        # Chrome DevTools용 요청은 그냥 무시 (응답 204)
        return Response(status_code=204)
    return await call_next(request)

# 프로젝트 초기용 코드입니다!
# @app.get("/")
# def read_root():
#     return {"message": "Hello, Blog Project!"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth as auth_router
from routers import post as post_router 

app = FastAPI()


origins = [
    "*", 
    "http://localhost",
    "http://localhost:8080", 
    "http://localhost:3000", # 일반적인 React/Vue 개발 서버 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 라우터 등록 ---
app.include_router(auth_router.router)
app.include_router(post_router.router)
#app.include_router(comment_router.router) # 💡 댓글 라우터 등록 완료

@app.get("/")
def read_root():
    return {"message": "Modu Blog API Server is running!"}
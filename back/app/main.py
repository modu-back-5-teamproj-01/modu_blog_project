from fastapi import FastAPI
# from routers import auth, posts

app = FastAPI()

# app.include_router(auth.router, prefix="/api")
# app.include_router(posts.router, prefix="/api")

# 프로젝트 초기용 코드입니다!
@app.get("/")
def read_root():
    return {"message": "Hello, Blog Project!"}
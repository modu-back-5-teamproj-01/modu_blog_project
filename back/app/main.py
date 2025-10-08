import sys
from pathlib import Path
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import auth
from routers import ai
from routers import post 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY가 .env 파일에 설정되어 있지 않습니다.")

DB_FILE = "db.jsonl"
USERS_FILE = "users.jsonl"
POSTS_FILE = "posts.jsonl"

app = FastAPI()

# 라우터 등록
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(post.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()
    if not os.path.exists(POSTS_FILE):
        open(POSTS_FILE, "w").close()

    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from routers import auth, posts

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api")

# back/app/schemas/post.py 파일 전체 내용

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# UserOut 스키마 임포트 (schemas 폴더 내의 user.py에서 가져옴)
# 이 임포트가 작동하려면 schemas/__init__.py가 제대로 되어 있어야 합니다.
from .user import UserOut 

# 게시물 생성/수정 요청 바디용 스키마
class PostCreate(BaseModel):
    title: str
    content: str

# 🚨 이 클래스 이름이 routers/post.py에서 'post_schema.Post'로 참조하는 것입니다.
class Post(BaseModel): 
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    
    # owner를 UserOut 스키마로 정의
    owner: UserOut 
    
    # Pydantic 설정 (SQLAlchemy ORM 호환성)
    class Config:
        orm_mode = True
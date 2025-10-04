from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .user import UserRead
from .tag import TagRead


class PostBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None


class PostCreate(PostBase):
    tags: Optional[List[str]] = None  # 태그 이름 목록으로 전달


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None


class PostRead(PostBase):
    id: int
    author: UserRead
    tags: Optional[List[TagRead]] = None
    view_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        orm_mode = True

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .user import UserRead


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    parent_comment_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentRead(CommentBase):
    id: int
    author: UserRead
    post_id: int
    parent_comment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    replies: Optional[List["CommentRead"]] = None  # 자기참조

    class Config:
        orm_mode = True
        from_attributes = True

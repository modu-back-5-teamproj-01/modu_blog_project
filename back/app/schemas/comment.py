# back/app/schemas/comment.py

from pydantic import BaseModel
from datetime import datetime

# ⭐ UserRead 대신 UserOut을 임포트합니다.
from .user import UserOut 

# ----------------------------------------------------------------------
# 댓글 생성 시 입력 스키마
class CommentCreate(BaseModel):
    post_id: int
    content: str
    parent_id: int | None = None # 대댓글용

# ----------------------------------------------------------------------
# 댓글 반환 시 출력 스키마
class CommentOut(BaseModel):
    id: int
    post_id: int
    content: str
    created_at: datetime
    # ⭐ UserRead 대신 UserOut 사용
    user: UserOut 
    parent_id: int | None = None

    class Config:
        # Pydantic V2 호환 설정
        from_attributes = True

# ----------------------------------------------------------------------
# 댓글 수정 시 입력 스키마
class CommentUpdate(BaseModel):
    content: str
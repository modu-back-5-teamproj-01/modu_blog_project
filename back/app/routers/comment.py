# back/app/routers/comment.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime 

# ... (다른 임포트)
from ..core.database import get_db
from ..models.comment import Comment as CommentModel
from ..models.post import Post as PostModel
from ..models.user import User as UserModel 

from ..schemas import comment as comment_schema
from ..schemas import user as user_schema

from .auth import get_current_user 

router = APIRouter(prefix="/comments", tags=["Comments"])


# 댓글 생성 엔드포인트
@router.post(
    "/", 
    # ⭐ 수정: CommentResponse -> CommentOut
    response_model=comment_schema.CommentOut, 
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    comment: comment_schema.CommentCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    # ... (함수 본문, 필요하다면 여기에 코드를 작성하세요)
    # 임시로 더미 객체를 리턴하여 FastAPI 로딩 테스트
    return comment_schema.CommentOut(
        id=1, 
        post_id=comment.post_id, 
        content=comment.content, 
        created_at=datetime.utcnow(),
        user=user_schema.UserOut(id=current_user.id, email=current_user.email, nickname=current_user.nickname, created_at=current_user.created_at),
        parent_id=comment.parent_id
    )
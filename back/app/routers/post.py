# back/app/routers/post.py 파일 전체 내용 (dependencies.py에서 임포트)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import post as post_schema
from ..models import post as post_model 
from ..models import user as user_model 

# 🚨 dependencies.py에서 get_current_user를 임포트합니다.
from ..dependencies import get_current_user 

router = APIRouter()

# 게시물 생성
@router.post("/", response_model=post_schema.Post, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post: post_schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: user_model.UserModel = Depends(get_current_user) 
):
    # 이제 순환 참조 없이 사용자 모델을 사용할 수 있습니다.
    return post
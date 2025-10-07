from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .models import user as user_model # 사용자 모델 임포트
from .core.database import get_db

# OAuth2 스키마 정의
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 🚨 이 함수를 모든 라우터가 임포트할 수 있도록 독립적인 파일로 분리합니다.
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 임시 사용자 ID 1번을 가정하고 반환 (실제 JWT 검증 로직 필요)
    user = db.query(user_model.UserModel).filter(user_model.UserModel.id == 1).first() 

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
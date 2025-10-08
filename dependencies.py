# back/app/dependencies.py 파일 전체 내용

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from back.app.core.database import get_db
from back.app.core.security import decode_access_token

# 2. models 임포트 문제 해결 (models/user.py 파일이 있다고 가정)
# 만약 user 모델이 back/app/models/user.py 에 있다면 아래처럼 작성합니다.
from back.app.models.user import UserModel 

# 🚨 OAuth2PasswordBearer 객체: JWT 토큰을 "Bearer" 스킴으로 기대합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") 

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    JWT 토큰을 검증하고 현재 로그인된 사용자 객체를 반환합니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 토큰 디코딩
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    # 토큰에서 사용자 이메일 (sub) 추출
    user_email: str = payload.get("sub")
    if user_email is None:
        raise credentials_exception
    
    # DB에서 사용자 객체 조회
    user = db.query(UserModel).filter(
        UserModel.email == user_email
    ).first()
    
    if user is None:
        raise credentials_exception
        
    return user
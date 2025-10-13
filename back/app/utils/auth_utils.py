import os
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError  # 설치 필요: pip install python-jose[cryptography]
import bcrypt
from app.models.user import User as UserModel
from app.models.session import Session as SessionModel
from app.core.database import get_db

# ---------------------------
# 비밀번호 해시/검증
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # bcrypt는 최대 72 bytes까지만 처리 가능
    # 문자열이 아니면 str로 변환
    # if not isinstance(password, str):
    #     password = str(password)
        
    # # 문자열 길이를 72로 제한 (문자 단위)
    # safe_password = password[:72]

    # return pwd_context.hash(safe_password)
    # 비밀번호가 str인지 확인
    if not isinstance(password, str):
        password = str(password)
    
     # UTF-8 바이트로 변환
    password_bytes = password.encode("utf-8")
    
    # 72바이트 초과 시 바이트 단위로 자르기
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        # 바이트를 다시 문자열로 변환 (깨진 문자는 무시)
        password = password_bytes.decode("utf-8", errors="ignore")
    
    # 해시 생성
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ---------------------------
# JWT 설정 (env 변수 활용)
# ---------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "replace-with-your-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(user_id: int, session_id: int, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": str(user_id), "sid": str(session_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int, session_id: int, expires_days: int = REFRESH_TOKEN_EXPIRE_DAYS) -> str:
    expire = datetime.utcnow() + timedelta(days=expires_days)
    payload = {"sub": str(user_id), "sid": str(session_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# ---------------------------
# 현재 사용자 조회
# ---------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    payload = decode_token(token)
    user_id: str = payload.get("sub")
    session_id: str = payload.get("sid")
    
    if user_id is None or session_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    # user 존재 확인
    user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # session 존재 확인
    session = db.query(SessionModel).filter(SessionModel.id == int(session_id), SessionModel.user_id == int(user.id)).first()
    if not session or session.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session is no longer valid")
    
    return user

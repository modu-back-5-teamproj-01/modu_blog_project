import sys
from pathlib import Path
import os
import json
import bcrypt
import jwt
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from datetime import datetime

# 💡 절대 경로 임포트: main.py의 sys.path 주입에 의존합니다.
from schemas.user import UserCreate, LoginRequest, TokenResponse
from core.security import get_current_user_email
# 환경 변수 및 파일 경로 설정
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY가 .env 파일에 설정되어 있지 않습니다.")

USERS_FILE = "users.json"
router = APIRouter(prefix="/api/auth", tags=["Auth"])

# --- 유틸리티 함수: JWT 및 파일 처리 ---

def find_user_by_email(email: str):
    """이메일을 통해 사용자 정보를 파일에서 검색"""
    if not os.path.exists(USERS_FILE):
        return None
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
            return next((u for u in users if u["email"] == email), None)
        except json.JSONDecodeError:
            return None

def save_user_to_db(user_data: dict):
    """새 사용자 정보를 파일에 저장"""
    users = []
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                pass
                
    users.append(user_data)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def create_access_token(data: dict):
    """JWT 토큰 생성"""
    to_encode = data.copy()
    # 토큰 만료 시간 설정 (예: 1시간)
    expire = datetime.utcnow() + timedelta(minutes=60) 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

from datetime import timedelta # create_access_token을 위해 추가

# --- 라우터 엔드포인트 구현 ---

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """새 사용자 등록 (회원가입)"""
    if find_user_by_email(user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일입니다.")

    # 비밀번호 해시
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    
    new_user = {
        "email": user_data.email,
        "username": user_data.username,
        "hashed_password": hashed_password.decode('utf-8')
    }
    
    save_user_to_db(new_user)
    return JSONResponse(content={"message": "회원가입이 완료되었습니다."}, status_code=status.HTTP_201_CREATED)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """사용자 로그인 및 JWT 토큰 발행"""
    user = find_user_by_email(credentials.email)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    # 비밀번호 검증
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), user["hashed_password"].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user["email"]})
    
    return TokenResponse(token=access_token)
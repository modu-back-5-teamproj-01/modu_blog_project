# modu_blog_project/back/app/routers/auth.py

import os
import json
import bcrypt
import jwt
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from datetime import datetime, timedelta # 💡 timedelta 임포트 추가
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

# 💡 절대 경로 임포트 (core/security.py)
from core.security import get_current_user_email, ALGORITHM

# --- Pydantic 스키마 정의 (다른 파일에 정의되어 있다면 제거하고 import로 대체) ---
class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str
    
class TokenResponse(BaseModel):
    token: str

class UserProfileResponse(BaseModel):
    email: str
    username: str

class UserProfileUpdate(BaseModel):
    username: str

class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

# --- 환경 변수 및 파일 경로 설정 ---
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY가 .env 파일에 설정되어 있지 않습니다.")

USERS_FILE = "users.json"
router = APIRouter(prefix="/api/auth", tags=["Auth"])

# --- JWT 및 파일 처리 유틸리티 ---

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

def save_users_to_db(users_list: list):
    """사용자 전체 리스트를 파일에 저장"""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_list, f, indent=4, ensure_ascii=False)

def create_access_token(data: dict):
    """JWT 토큰 생성"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60) 
    to_encode.update({"exp": expire.timestamp()}) # 💡 timestamp()로 통일
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # 💡 ALGORITHM 사용
    return encoded_jwt

# --- 블랙리스트 및 보안 설정 ---
TOKEN_BLACKLIST = set() # 💡 TOKEN_BLACKLIST 정의는 auth.py에 유지
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login") 

# --- 라우터 엔드포인트 구현 ---

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """새 사용자 등록 (회원가입)"""
    if find_user_by_email(user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일입니다.")

    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    
    users = []
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                pass
                
    new_user = {
        "email": user_data.email,
        "username": user_data.username,
        "hashed_password": hashed_password.decode('utf-8')
    }
    
    users.append(new_user)
    save_users_to_db(users) 
    return JSONResponse(content={"message": "회원가입이 완료되었습니다."}, status_code=status.HTTP_201_CREATED)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """사용자 로그인 및 JWT 토큰 발행"""
    user = find_user_by_email(credentials.email)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    if not bcrypt.checkpw(credentials.password.encode('utf-8'), user["hashed_password"].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    # core/security.py의 create_access_token 대신 여기서 정의한 함수 사용
    access_token = create_access_token(data={"sub": user["email"]})
    
    return TokenResponse(token=access_token)

@router.delete("/logout", status_code=status.HTTP_200_OK)
async def logout(
    token: str = Depends(oauth2_scheme), 
):
    """사용자의 현재 액세스 토큰을 블랙리스트에 추가하여 무효화합니다."""
    if token in TOKEN_BLACKLIST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 로그아웃 처리된 토큰입니다."
        )

    TOKEN_BLACKLIST.add(token)
    return {"message": "로그아웃 성공. 토큰이 무효화되었습니다."}

# --- 신규 구현 엔드포인트 ---

@router.get("/me", response_model=UserProfileResponse)
async def read_users_me(
    current_user_email: str = Depends(get_current_user_email)
):
    """현재 로그인된 사용자의 정보를 조회합니다."""
    user_data = find_user_by_email(current_user_email)
    
    if not user_data:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다. 인증 오류.")

    return UserProfileResponse(email=user_data["email"], username=user_data["username"])


@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    new_profile: UserProfileUpdate,
    current_user_email: str = Depends(get_current_user_email)
):
    """현재 로그인된 사용자의 프로필(닉네임)을 수정합니다."""
    users = []
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                pass
    
    found = False
    
    for i, user in enumerate(users):
        if user["email"] == current_user_email:
            users[i]["username"] = new_profile.username
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    save_users_to_db(users)
    
    return UserProfileResponse(email=current_user_email, username=new_profile.username)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    data: UserPasswordUpdate,
    current_user_email: str = Depends(get_current_user_email)
):
    """현재 로그인된 사용자의 비밀번호를 변경합니다."""
    users = []
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                pass
    
    found = False
    
    for i, user in enumerate(users):
        if user["email"] == current_user_email:
            # 1. 기존 비밀번호 확인
            if not bcrypt.checkpw(data.old_password.encode('utf-8'), user["hashed_password"].encode('utf-8')):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="기존 비밀번호가 일치하지 않습니다."
                )
            
            # 2. 새 비밀번호 해시 및 저장
            users[i]["hashed_password"] = bcrypt.hashpw(data.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            found = True
            break
            
    if not found:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    save_users_to_db(users)
    return
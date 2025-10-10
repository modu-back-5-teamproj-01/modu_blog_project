# modu_blog_project/back/app/routers/auth.py

import os
import json
import bcrypt
import jwt as jwt_lib # 💡 jwt 라이브러리를 안전하게 임포트
import calendar 
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone 
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

# 💡 core/security에서 get_current_user_email만 임포트합니다.
from core.security import get_current_user_email

# --- 환경 변수 및 파일 경로 설정 ---
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY") 
if not SECRET_KEY:
    raise ValueError("SECRET_KEY가 .env 파일에 설정되어 있지 않습니다.")

ALGORITHM = "HS256"

# --- Pydantic 스키마 정의 (생략) ---
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

# --- 파일 경로 및 라우터 설정 ---
USERS_FILE = "users.json"
router = APIRouter(prefix="/api/auth", tags=["Auth"])

# --- 파일 처리 유틸리티 (생략) ---
def find_user_by_email(email: str):
    if not os.path.exists(USERS_FILE): return None
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
            return next((u for u in users if u["email"] == email), None)
        except json.JSONDecodeError: return None

def save_users_to_db(users_list: list):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_list, f, indent=4, ensure_ascii=False)


# --- JWT 토큰 생성 ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24) 
    to_encode.update({"exp": calendar.timegm(expire.timetuple())})
    
    # 💡 jwt_lib 사용
    encoded_jwt = jwt_lib.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    return encoded_jwt

# --- 블랙리스트 및 보안 설정 ---
TOKEN_BLACKLIST = set() 
# 💡 core/security.py가 이 객체를 임포트합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login") 

# --- 라우터 엔드포인트 구현 (생략) ---

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    if find_user_by_email(user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일입니다.")

    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    
    users = []
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try: users = json.load(f)
            except json.JSONDecodeError: pass
                
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
    user = find_user_by_email(credentials.email)
    
    if not user or not bcrypt.checkpw(credentials.password.encode('utf-8'), user["hashed_password"].encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    access_token = create_access_token(data={"sub": user["email"]})
    
    return TokenResponse(token=access_token) 

@router.delete("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str = Depends(oauth2_scheme)):
    if token in TOKEN_BLACKLIST:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 로그아웃 처리된 토큰입니다.")

    TOKEN_BLACKLIST.add(token)
    return {"message": "로그아웃 성공. 토큰이 무효화되었습니다."}

@router.get("/me", response_model=UserProfileResponse)
async def read_users_me(current_user_email: str = Depends(get_current_user_email)):
    user_data = find_user_by_email(current_user_email)
    if not user_data:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다. 인증 오류.")
    return UserProfileResponse(email=user_data["email"], username=user_data["username"])

@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(new_profile: UserProfileUpdate, current_user_email: str = Depends(get_current_user_email)):
    users = []
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try: users = json.load(f)
            except json.JSONDecodeError: pass
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
async def update_user_password(data: UserPasswordUpdate, current_user_email: str = Depends(get_current_user_email)):
    users = []
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try: users = json.load(f)
            except json.JSONDecodeError: pass
    found = False
    for i, user in enumerate(users):
        if user["email"] == current_user_email:
            if not bcrypt.checkpw(data.old_password.encode('utf-8'), user["hashed_password"].encode('utf-8')):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="기존 비밀번호가 일치하지 않습니다.")
            users[i]["hashed_password"] = bcrypt.hashpw(data.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    save_users_to_db(users)
    return
# back/app/core/security.py 파일 전체 내용 (필요한 경우 생성)

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError

# --- 환경 설정 ---
# 비밀번호 해싱 알고리즘 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 설정 (보안을 위해 SECRET_KEY는 환경 변수에서 로드해야 합니다.)
# 🚨 임시 키입니다. 실제 환경에서는 환경 변수를 사용하세요.
SECRET_KEY = "your-super-secret-key-that-should-be-in-env" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


# --- 1. 비밀번호 해싱 ---
def hash_password(password: str) -> str:
    """비밀번호를 해싱합니다."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 해싱된 비밀번호를 비교합니다."""
    return pwd_context.verify(plain_password, hashed_password)


# --- 2. JWT 토큰 생성 ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """액세스 토큰을 생성합니다."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 30분 후 만료 설정
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- 3. JWT 데이터 디코딩 ---
def decode_access_token(token: str) -> Optional[dict]:
    """액세스 토큰에서 데이터를 디코딩합니다."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
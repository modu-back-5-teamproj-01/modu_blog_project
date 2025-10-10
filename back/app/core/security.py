import os
import jwt as jwt_lib 
from fastapi import Depends, HTTPException, status
# 💡 APIKeyHeader를 사용하도록 변경
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader 
from dotenv import load_dotenv

# --- 환경 변수 직접 로드 및 SECRET_KEY 정의 ---
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY가 .env 파일에 설정되어 있지 않습니다.")

ALGORITHM = "HS256"

# 💡 토큰 직접 입력 방식을 위한 APIKeyHeader 정의
# 이는 Swagger UI에서 '토큰 문자열'을 직접 입력하는 칸을 만들어줍니다.
oauth2_scheme = APIKeyHeader(name="Authorization", scheme_name="Bearer", auto_error=True)

# 💡 TOKEN_BLACKLIST만 auth 라우터에서 임포트
try:
    from routers.auth import TOKEN_BLACKLIST
except ImportError:
    TOKEN_BLACKLIST = set()


async def get_current_user_email(token: str = Depends(oauth2_scheme)):
    """
    JWT 토큰을 검증하고 사용자 이메일(sub)을 추출합니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없거나 토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 💡 APIKeyHeader를 사용하면 토큰이 "Bearer xxx" 형태로 들어오므로, "Bearer " 접두사 제거
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    
    # 1. 블랙리스트 확인
    if token in TOKEN_BLACKLIST:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 무효화(로그아웃)되었습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. JWT 디코딩 로직 실행
    try:
        payload = jwt_lib.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        
        if user_email is None:
            raise credentials_exception
            
    except jwt_lib.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다.", 
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt_lib.InvalidTokenError:
        raise credentials_exception
        
    return user_email
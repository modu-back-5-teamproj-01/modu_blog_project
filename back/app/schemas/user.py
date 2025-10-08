from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """기본 사용자 정보 (이메일, 사용자명)"""
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """회원가입 요청 데이터 (비밀번호 포함)"""
    password: str

class LoginRequest(BaseModel):
    """로그인 요청 데이터"""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """로그인 성공 응답 데이터 (JWT 토큰 반환)"""
    token: str
    message: str = "로그인 성공"

class UserInDB(UserBase):
    """DB 저장 시 사용할 모델 (비밀번호는 해시된 문자열)"""
    hashed_password: str

class UserOut(UserBase):
    """외부(게시물 등)에 사용자 정보를 노출할 때 사용하는 안전한 모델 (비밀번호 제외)"""
    # email과 username은 UserBase에서 상속받음
    
    class Config:
        # Pydantic 2.0+ 버전에서 ORM 모드(딕셔너리 대신 객체에서 데이터 로딩) 지원을 위해 사용
        from_attributes = True
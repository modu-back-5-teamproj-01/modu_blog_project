# back/app/schemas/user.py 파일 전체 내용

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional # bio를 위해 Optional 타입을 추가합니다.

# 요청 바디용 스키마 (회원가입 시 사용)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    bio: Optional[str] = None # Optional 사용

# 응답용 스키마 (다른 파일에서 UserOut으로 임포트하도록 통일)
class UserOut(BaseModel): 
    id: int
    username: str
    email: EmailStr
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Pydantic 설정
    class Config:
        orm_mode = True
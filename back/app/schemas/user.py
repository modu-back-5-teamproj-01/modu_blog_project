from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    password: str

# 현재 사실상 사용처가 없음(session.py의 UserProfileUpdate 클래스를 사용하길 권장)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

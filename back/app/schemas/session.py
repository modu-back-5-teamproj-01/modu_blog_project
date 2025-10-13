from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# --------------------
# Session (DB 연동용)
# --------------------
class SessionBase(BaseModel):
    user_id: int
    refresh_token_hash: str
    issued_at: datetime
    expires_at: datetime
    revoked: bool = False

class SessionCreate(BaseModel):
    user_id: int
    refresh_token_hash: str
    expires_at: datetime

class SessionRead(SessionBase):
    id: int
    class Config:
        orm_mode = True


# --------------------
# Auth (요청/응답용)
# --------------------
class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None

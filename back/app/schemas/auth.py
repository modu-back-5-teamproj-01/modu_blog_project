from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from back.app.core import get_db
from back.app.models import User
from back.app.schemas import UserCreate

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # orm_mode → from_attributes

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
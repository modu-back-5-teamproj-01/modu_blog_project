from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):  # 이 클래스가 없어서 에러 발생
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # orm_mode 대신 from_attributes 사용 (Pydantic V2)
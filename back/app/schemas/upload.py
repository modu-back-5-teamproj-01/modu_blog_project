from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UploadBase(BaseModel):
    file_name: str
    content_type: str


class UploadCreate(UploadBase):
    post_id: Optional[int] = None


class UploadRead(UploadBase):
    id: int
    uploader_id: int
    post_id: Optional[int]
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True

# modu_blog_project/back/app/routers/comment.py (추가된 댓글 라우터)

import os
import json
from uuid import uuid4
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

from core.security import get_current_user_email

# --- 파일 경로 설정 ---
COMMENTS_FILE = "comments.json"
router = APIRouter(prefix="/api/comments", tags=["Comments"])

# --- Pydantic 스키마 정의 ---
class CommentCreate(BaseModel):
    post_id: str = Field(..., description="댓글을 달 게시물의 ID")
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: str
    post_id: str
    content: str
    author_email: str
    created_at: datetime
    updated_at: datetime | None = None

# --- 유틸리티 함수: 파일 처리 ---
def load_comments():
    if not os.path.exists(COMMENTS_FILE) or os.path.getsize(COMMENTS_FILE) == 0:
        return []
    with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_comments(comments_list: list):
    with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(comments_list, f, indent=4, ensure_ascii=False)

# --- 라우터 엔드포인트 구현 (CRUD) ---

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    current_user_email: str = Depends(get_current_user_email)
):
    comments = load_comments()
    
    new_comment = {
        "id": str(uuid4()),
        "post_id": comment_data.post_id,
        "content": comment_data.content,
        "author_email": current_user_email,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
    }
    
    comments.append(new_comment)
    save_comments(comments)
    
    return new_comment

@router.get("/{post_id}", response_model=list[CommentResponse])
async def read_comments_by_post(post_id: str):
    all_comments = load_comments()
    post_comments = [c for c in all_comments if c["post_id"] == post_id]
    return post_comments

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: str,
    comment_data: CommentUpdate,
    current_user_email: str = Depends(get_current_user_email)
):
    comments = load_comments()
    for i, comment in enumerate(comments):
        if comment["id"] == comment_id:
            if comment["author_email"] != current_user_email:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="댓글 수정 권한이 없습니다.")
            comments[i]["content"] = comment_data.content
            comments[i]["updated_at"] = datetime.now().isoformat()
            save_comments(comments)
            return comments[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다.")

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: str,
    current_user_email: str = Depends(get_current_user_email)
):
    comments = load_comments()
    comment_index = next((i for i, c in enumerate(comments) if c["id"] == comment_id), None)
    
    if comment_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다.")
        
    comment_to_delete = comments[comment_index]
    if comment_to_delete["author_email"] != current_user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="댓글 삭제 권한이 없습니다.")

    del comments[comment_index]
    save_comments(comments)
    return
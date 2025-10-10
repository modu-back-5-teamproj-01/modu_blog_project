# modu_blog_project/back/app/routers/post.py

import os
import json
from uuid import uuid4
from fastapi import APIRouter, Depends, status, HTTPException, Path
from pydantic import BaseModel, Field
from datetime import datetime

from core.security import get_current_user_email

# --- 파일 경로 설정 ---
POSTS_FILE = "posts.json"
COMMENTS_FILE = "comments.json" 
router = APIRouter(prefix="/api/posts", tags=["Posts"])

# --- Pydantic 스키마 정의 ---

class CommentCreate(BaseModel):
    """댓글 생성 요청 스키마 (post_id는 URL에서 받음)"""
    content: str

class CommentUpdate(BaseModel):
    """댓글 수정 요청 스키마"""
    content: str

class CommentResponse(BaseModel):
    """댓글 응답 스키마"""
    id: str
    post_id: str
    content: str
    author_email: str
    created_at: datetime
    updated_at: datetime | None = None

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostResponse(BaseModel):
    """게시물 응답 스키마 (댓글 목록 포함)"""
    id: str
    title: str
    content: str
    author_email: str
    created_at: datetime
    updated_at: datetime | None = None
    comments: list[CommentResponse] 

# --- 유틸리티 함수: 파일 처리 ---

def load_posts():
    if not os.path.exists(POSTS_FILE) or os.path.getsize(POSTS_FILE) == 0: return []
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except json.JSONDecodeError: return []

def save_posts(posts_list: list):
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts_list, f, indent=4, ensure_ascii=False)

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


# ----------------------------------------------------------------------
# 🚀 게시물 라우터 엔드포인트 (Posts CRUD)
# ----------------------------------------------------------------------

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user_email: str = Depends(get_current_user_email) 
):
    """새 게시물 생성 (C)"""
    posts = load_posts()
    
    new_post = {
        "id": str(uuid4()),
        "title": post_data.title,
        "content": post_data.content,
        "author_email": current_user_email,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
    }
    
    posts.append(new_post)
    save_posts(posts)
    
    # PostResponse 스키마 형식을 맞추기 위해 빈 comments 목록을 추가하여 반환
    return {**new_post, "comments": []} 

@router.get("/", response_model=list[PostResponse])
async def read_posts():
    """전체 게시물 목록을 조회합니다. (댓글은 포함하지 않음)"""
    all_posts = load_posts()
    
    # 목록 조회 시에도 PostResponse 스키마를 만족시키기 위해 빈 comments 목록을 추가
    response_posts = []
    for post in all_posts:
        response_posts.append({**post, "comments": []})
        
    return response_posts


@router.get("/{post_id}", response_model=PostResponse)
async def read_post(post_id: str):
    """특정 게시물 상세 정보와 댓글을 함께 조회합니다. (R)"""
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")

    all_comments = load_comments()
    post_comments = [c for c in all_comments if c["post_id"] == post_id]
    
    post_with_comments = {**post, "comments": post_comments}
        
    return post_with_comments


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    current_user_email: str = Depends(get_current_user_email) 
):
    """특정 게시물 수정 (U)"""
    posts = load_posts()
    
    for i, post in enumerate(posts):
        if post["id"] == post_id:
            if post["author_email"] != current_user_email:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="게시물 수정 권한이 없습니다.")
            
            posts[i]["title"] = post_data.title if post_data.title is not None else post["title"]
            posts[i]["content"] = post_data.content if post_data.content is not None else post["content"]
            posts[i]["updated_at"] = datetime.now().isoformat()
            
            save_posts(posts)
            
            # 수정 후에도 댓글 목록을 포함하여 반환
            all_comments = load_comments()
            post_comments = [c for c in all_comments if c["post_id"] == post_id]
            
            return {**posts[i], "comments": post_comments}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user_email: str = Depends(get_current_user_email)
):
    """특정 게시물 삭제 (D)"""
    posts = load_posts()
    
    post_index = next((i for i, p in enumerate(posts) if p["id"] == post_id), None)
    
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")
        
    post_to_delete = posts[post_index]

    if post_to_delete["author_email"] != current_user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="게시물 삭제 권한이 없습니다.")

    del posts[post_index]
    save_posts(posts)
    
    return
    
# ----------------------------------------------------------------------
# 🚀 댓글 라우터 (게시물에 중첩 - /api/posts/{post_id}/comments)
# ----------------------------------------------------------------------

@router.post("/{post_id}/comments/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: str = Path(..., description="댓글을 달 게시물의 ID"),
    comment_data: CommentCreate = Depends(), 
    current_user_email: str = Depends(get_current_user_email)
):
    """특정 게시물에 새 댓글 생성 (C)"""
    posts = load_posts()
    if not next((p for p in posts if p["id"] == post_id), None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 달 게시물을 찾을 수 없습니다.")
    
    comments = load_comments()
    
    new_comment = {
        "id": str(uuid4()),
        "post_id": post_id, 
        "content": comment_data.content,
        "author_email": current_user_email,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
    }
    
    comments.append(new_comment)
    save_comments(comments)
    
    return new_comment

@router.get("/{post_id}/comments/", response_model=list[CommentResponse])
async def read_comments_by_post(post_id: str):
    """특정 게시물의 모든 댓글 조회 (R)"""
    posts = load_posts()
    if not next((p for p in posts if p["id"] == post_id), None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 조회할 게시물을 찾을 수 없습니다.")
        
    all_comments = load_comments()
    post_comments = [c for c in all_comments if c["post_id"] == post_id]
    
    return post_comments


@router.put("/{post_id}/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    post_id: str = Path(..., description="게시물 ID"),
    comment_id: str = Path(..., description="수정할 댓글 ID"),
    comment_data: CommentUpdate = Depends(),
    current_user_email: str = Depends(get_current_user_email)
):
    """특정 게시물의 특정 댓글 수정 (U)"""
    comments = load_comments()
    
    for i, comment in enumerate(comments):
        if comment["id"] == comment_id and comment["post_id"] == post_id:
            if comment["author_email"] != current_user_email:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="댓글 수정 권한이 없습니다."
                )
            comments[i]["content"] = comment_data.content
            comments[i]["updated_at"] = datetime.now().isoformat()
            
            save_comments(comments)
            return comments[i]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물에 속한 댓글을 찾을 수 없습니다.")


@router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    post_id: str = Path(..., description="게시물 ID"),
    comment_id: str = Path(..., description="삭제할 댓글 ID"),
    current_user_email: str = Depends(get_current_user_email)
):
    """특정 게시물의 특정 댓글 삭제 (D)"""
    comments = load_comments()
    
    comment_index = next((i for i, c in enumerate(comments) if c["id"] == comment_id and c["post_id"] == post_id), None)
    
    if comment_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물에 속한 댓글을 찾을 수 없습니다.")
        
    comment_to_delete = comments[comment_index]

    if comment_to_delete["author_email"] != current_user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="댓글 삭제 권한이 없습니다."
        )

    del comments[comment_index]
    save_comments(comments)
    
    return
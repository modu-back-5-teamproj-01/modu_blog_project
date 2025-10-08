import sys
from pathlib import Path
import json
import os
import uuid
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime

from schemas.post import PostCreate, PostUpdate, PostResponse
from core.security import get_current_user_email # jwt 인증 함수 임포트

router = APIRouter(prefix="/api/posts", tags=["Post"])
POSTS_FILE = "posts.jsonl" 

# --- 유틸리티 함수: 데이터 파일 처리 ---

def load_posts():
    """파일에서 모든 게시물을 로드"""
    posts = []
    # 파일이 없으면 빈 파일 생성
    if not os.path.exists(POSTS_FILE):
        open(POSTS_FILE, "w").close()
        return posts
    
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                posts.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return posts

def save_posts(posts):
    """게시물 목록을 파일에 저장"""
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        for post in posts:
            f.write(json.dumps(post, ensure_ascii=False, default=str) + "\n")
            
# --- 라우터 엔드포인트 구현 ---

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    # 💡 JWT 인증 적용: 토큰이 없거나 유효하지 않으면 401 UNAUTHORIZED 반환
    current_user_email: str = Depends(get_current_user_email)
):
    """새 게시물 생성 (로그인 사용자만 가능)"""
    current_time = datetime.now()
    
    # PostCreate 스키마 데이터를 딕셔너리로 변환하고 추가 정보 삽입
    new_post_data = post.model_dump() 
    new_post_data.update({
        "post_id": str(uuid.uuid4()),
        "author_email": current_user_email, # JWT에서 추출한 이메일을 작성자로 설정
        "created_at": current_time.isoformat(),
        "updated_at": current_time.isoformat()
    })
    
    posts = load_posts()
    posts.append(new_post_data)
    save_posts(posts)
    
    return new_post_data

@router.get("/", response_model=List[PostResponse])
async def read_posts():
    """모든 게시물 목록 조회"""
    posts = load_posts()
    # 최신 글이 위로 오도록 역순으로 정렬
    return posts[::-1]

@router.get("/{post_id}", response_model=PostResponse)
async def read_post(post_id: str):
    """특정 게시물 상세 조회"""
    posts = load_posts()
    # post_id가 일치하는 게시물 검색
    post = next((p for p in posts if p.get("post_id") == post_id), None)
    
    if post is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")
        
    return post
    
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user_email: str = Depends(get_current_user_email) # 권한 체크
):
    """게시물 삭제 (작성자만 가능)"""
    posts = load_posts()
    
    # 1. 게시물 찾기
    post_to_delete = next((p for p in posts if p.get("post_id") == post_id), None)

    if post_to_delete is None:
        raise HTTPException(status_code=404, detail="삭제할 게시물을 찾을 수 없습니다.")

    # 2. 권한 확인: JWT에서 추출한 이메일과 작성자 이메일 비교
    if post_to_delete["author_email"] != current_user_email:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
        
    # 3. 삭제 실행
    new_posts = [p for p in posts if p["post_id"] != post_id]
    save_posts(new_posts)
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "삭제 완료"})
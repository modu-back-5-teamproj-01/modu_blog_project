# routers/blog.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime

from app.models.post import Post as PostModel
from app.models.post_tag import PostTag as PostTagModel
from app.models.tag import Tag as TagModel
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.schemas.user import UserRead
from app.schemas.tag import TagRead
from app.core.database import get_db
from app.utils import auth_utils

router = APIRouter(prefix="/blog", tags=["Blog"])

# ----------------------------
# 유틸: DB 객체 -> Pydantic 변환
# ----------------------------
def map_post_to_postread(post: PostModel) -> PostRead:
    return PostRead(
        id=post.id,
        title=post.title,
        content=post.content,
        summary=post.summary,
        author=UserRead(
            id=post.author.id,
            username=post.author.username,
            created_at=post.author.created_at,
            updated_at=post.author.updated_at,
        ),
        tags=[TagRead(id=pt.tag.id, name=pt.tag.name) for pt in post.tags],
        created_at=post.created_at,
        updated_at=post.updated_at,
        view_count=post.view_count,
    )

# ----------------------------
# 게시글 작성
# ----------------------------
@router.post("/", response_model=PostRead)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_user),
):
    # 새 Post 객체 생성
    post = PostModel(
        title=post_in.title,
        content=post_in.content,
        summary=post_in.summary,
        author_id=current_user.id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    # 태그 연결
    if post_in.tags:
        for tag_name in post_in.tags:
            # db에 태그가 있는지 확인
            tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
            
            # db에 태그가 없으면 새로 생성
            if not tag:
                tag = TagModel(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
                
            # PostTag 연결 생성
            post_tag = PostTagModel(post_id=post.id, tag_id=tag.id)
            db.add(post_tag)
        db.commit()
        db.refresh(post)

    return map_post_to_postread(post)

# ----------------------------
# 게시글 목록 + 검색 + 정렬
# ----------------------------
@router.get("/", response_model=List[PostRead])
def list_posts(
    search: Optional[str] = Query(None),
    sort: str = Query("desc"),
    skip: int = Query(0),
    limit: int = Query(10),
    db: Session = Depends(get_db),
):
    query = db.query(PostModel).options(
        joinedload(PostModel.author),   # 작성자 정보 미리 로딩
        joinedload(PostModel.tags).joinedload(PostTagModel.tag) # 태그 정보 미리 로딩
    )
    
    # 검색어 필터
    if search:
        query = query.filter(PostModel.title.contains(search))
        
    # 정렬
    if sort == "asc":
        query = query.order_by(PostModel.created_at.asc())
    else:
        query = query.order_by(PostModel.created_at.desc())
    
    # 페이지네이션
    posts = query.offset(skip).limit(limit).all()
    
    return [map_post_to_postread(post) for post in posts]

# ----------------------------
# 게시글 태그 조회
# ----------------------------
@router.get("/tag/{tag_name}", response_model=List[PostRead])
def posts_by_tag(tag_name: str, db: Session = Depends(get_db)):
    # 태그 이름으로 TagModel 조회
    tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
    
    # 태그가 없으면 빈 리스트 반환
    if not tag:
        return []
    
    # PostTagModel에서 해당 태그와 연결된 게시글 ID 조회
    # joinedload 사용해서 Post와 관련된 작성자/태그 한 번에 로딩
    post_tags = db.query(PostTagModel).options(
                joinedload(PostTagModel.post).joinedload(PostModel.author),
                joinedload(PostTagModel.post).joinedload(PostModel.tags)
                ).filter(PostTagModel.tag_id == tag.id).all()

    posts = [map_post_to_postread(pt.post) for pt in post_tags]
    # post_tags = db.query(PostTagModel).filter(PostTagModel.tag_id == tag.id).all()
    # PostModel에서 게시글 ID로 게시글 조회
    # posts = [db.query(PostModel).get(pt.post_id) for pt in post_tags]
    return posts

# ----------------------------
# 게시글 상세보기
# ----------------------------
@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, db: Session = Depends(get_db)):
    # post_id로 PostModel 조회
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return map_post_to_postread(post)

# ----------------------------
# 게시글 수정
# ----------------------------
@router.put("/{post_id}", response_model=PostRead)
def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_user),
):
    # 게시글 존재 확인
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # 작성자 확인
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 본문/제목/요약 업데이트. 전달된 값이 있는 필드만 업데이트
    if post_in.title:
        post.title = post_in.title
    if post_in.content:
        post.content = post_in.content
    if post_in.summary:
        post.summary = post_in.summary
    # update_at 필드 갱신
    post.updated_at = datetime.now()
    db.commit()
    db.refresh(post)

    # 태그 업데이트
    if post_in.tags is not None:
        # 기존 태그 삭제
        db.query(PostTagModel).filter(PostTagModel.post_id == post.id).delete()
        db.commit()
        for tag_name in post_in.tags:
            # 전달된 각 태그가 db에 있는지 확인(이름으로 확인)
            tag = db.query(TagModel).filter(TagModel.name == tag_name).first()
            # db에 태그가 존재하지 않으면 새로 생성
            if not tag:
                tag = TagModel(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            # PostTag 테이블에 연결 추가
            post_tag = PostTagModel(post_id=post.id, tag_id=tag.id)
            db.add(post_tag)
        db.commit()
        db.refresh(post)

    return map_post_to_postread(post)

# ----------------------------
# 게시글 삭제
# ----------------------------
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_user),
):
    # 게시글 존재 여부 확인
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 작성자 확인
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # 관련 PostTag 삭제
    db.query(PostTagModel).filter(PostTagModel.post_id == post.id).delete()
    # 게시글 삭제
    db.delete(post)
    db.commit()
    return {"detail": f"Post {post_id} deleted successfully"}

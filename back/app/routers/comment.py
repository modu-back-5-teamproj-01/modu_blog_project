# routers/comment.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from app.models.comment import Comment as CommentModel
from app.models.post import Post as PostModel
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from app.schemas.user import UserRead
from app.utils.auth_utils import get_current_user
from app.core.database import get_db

router = APIRouter(prefix="/blog/{post_id}/comments", tags=["Comment"])

# ----------------------------
# DB 객체 -> Pydantic 모델 변환
# ----------------------------
def map_comment_to_read(comment: CommentModel) -> CommentRead:
    return CommentRead(
        id=comment.id,
        author=UserRead(
            id=comment.author.id,
            username=comment.author.username,
            email=comment.author.email,
            bio=comment.author.bio,
            created_at=comment.author.created_at,
            updated_at=comment.author.updated_at,
        ),
        post_id=comment.post_id,
        parent_comment_id=comment.parent_comment_id,
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        replies=[map_comment_to_read(reply) for reply in comment.replies] if comment.replies else []
    )

# ----------------------------
# 댓글 목록 조회
# ----------------------------
@router.get("/", response_model=List[CommentRead])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(CommentModel).options(
        joinedload(CommentModel.author),    # 댓글 작성자 정보 로딩
        joinedload(CommentModel.replies).joinedload(CommentModel.author)    # 해당 댓글의 대댓글과 대댓글 작성자 정보 로딩
    ).filter(
        CommentModel.post_id == post_id,
        CommentModel.parent_comment_id == None  # 최상위 댓글만 가져오기
    ).all()
    return [map_comment_to_read(c) for c in comments]

# ----------------------------
# 댓글 작성
# ----------------------------
@router.post("/", response_model=CommentRead)
def create_comment(
    post_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # post 존재 확인
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = CommentModel(
        post_id=post_id,
        author_id=current_user.id,
        content=comment_in.content,
        parent_comment_id=None, # 최상위 댓글
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(comment)
    db.commit()
    db.refresh(comment) # DB 갱신
    return map_comment_to_read(comment)

# ----------------------------
# 댓글 수정
# ----------------------------
@router.put("/{comment_id}", response_model=CommentRead)
def update_comment(
    post_id: int,
    comment_id: int,
    comment_in: CommentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id, CommentModel.post_id == post_id).first()
    # 댓글 존재 확인
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    # 댓글 작성자 본인인지 확인
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if comment_in.content:
        comment.content = comment_in.content
        comment.updated_at = datetime.now() # 수정 후 수정 시간 갱신
        db.commit()
        db.refresh(comment)
    
    return map_comment_to_read(comment)

# ----------------------------
# 댓글 삭제 (하위 대댓글도 삭제)
# ----------------------------
@router.delete("/{comment_id}")
def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id, CommentModel.post_id == post_id).first()
    # 댓글 존재 확인
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    # 댓글 작성자 본인인지 확인
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 하위 대댓글 삭제
    db.query(CommentModel).filter(CommentModel.parent_comment_id == comment.id).delete()
    db.delete(comment)
    db.commit()

    return {"detail": f"Comment {comment_id} and its replies deleted successfully"}

# ----------------------------
# 대댓글 작성
# ----------------------------
@router.post("/{comment_id}/replies", response_model=CommentRead)
def create_reply(
    post_id: int,
    comment_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    parent_comment = db.query(CommentModel).filter(CommentModel.id == comment_id, CommentModel.post_id == post_id).first()
    # 부모 댓글 존재하는지 확인
    if not parent_comment:
        raise HTTPException(status_code=404, detail="Parent comment not found")
    # 대댓글의 대댓글 방지
    if parent_comment.parent_comment_id is not None:
        raise HTTPException(status_code=400, detail="Cannot reply to a reply")  # 대대댓글 방지

    reply = CommentModel(
        post_id=post_id,
        author_id=current_user.id,
        content=comment_in.content,
        parent_comment_id=parent_comment.id,    # 부모 댓글 ID 설정
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(reply)
    db.commit()
    db.refresh(reply)
    return map_comment_to_read(reply)

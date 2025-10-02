from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, schemas, models


router = APIRouter(prefix="/posts", tags=["Posts"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    # TODO: 여기에서 OpenAI API를 호출하여 요약 및 태그 생성 로직 추가 !
    return db_post


# READ (게시글 목록 조회)
@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# READ (게시글 상세 조회)
@router.get("/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


# UPDATE (게시글 수정)
@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int, post_data: schemas.PostUptate, db: Session = Depends(get_db)
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    for key, value in post_data.dict(exclude_unset=True).items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post


# DELETE (게시글 삭제)
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db.post)
    db.commit()
    return {"message": "Post deleted successfully"}

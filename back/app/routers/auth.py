# back/app/routers/auth.py 파일 전체 내용 (get_current_user 제거)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import user as user_schema
from ..models import user as user_model
from ..core.security import hash_password, verify_password
from ..core.database import get_db
# 🚨 dependencies.py에서 get_current_user를 가져오지 않도록 합니다 (auth 라우터는 필요 없음)

router = APIRouter()

# 회원가입 (POST /auth/signup) 
@router.post("/signup", response_model=user_schema.UserOut) 
# ... (create_user 함수 내용은 그대로 유지)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    if db.query(user_model.UserModel).filter((user_model.UserModel.username == user.username) | (user_model.UserModel.email == user.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")

    hashed_password = hash_password(user.password)

    db_user = user_model.UserModel(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        bio=user.bio 
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 로그인 (POST /auth/login)
@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return {"access_token": "fake_token_for_now", "token_type": "bearer"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
import datetime
import os
from app.models.user import User as UserModel
from app.models.session import Session as SessionModel
from app.schemas.session import (
    UserRegister,
    UserLogin,
    UserProfileUpdate,
    PasswordChange,
    TokenResponse,
)
from app.schemas.user import UserRead
from app.core.database import get_db
from app.utils import auth_utils

router = APIRouter(prefix="/auth", tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30))

# ----------------------------
# 회원가입
# ----------------------------
@router.post("/register", response_model=UserRead)
def register(user_in: UserRegister, db: Session = Depends(get_db)) -> Any:
    # username 중복 확인
    existing = db.query(UserModel).filter(UserModel.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = auth_utils.hash_password(user_in.password)
    user = UserModel(
        username=user_in.username,
        password_hash=hashed_password,
        email=user_in.email,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return user

# ----------------------------
# 로그인
# ----------------------------
@router.post("/login", response_model=TokenResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)) -> Any:
    user = db.query(UserModel).filter(UserModel.username == user_in.username).first()
    if not user or not auth_utils.verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    
    now = datetime.datetime.now()
    expires_at = now + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # 새 세션 생성
    session = SessionModel(
        user_id=user.id,
        refresh_token_hash="", # 나중에 채움
        issued_at=now,
        expires_at=expires_at,
        revoked=False
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # 토큰 생성
    access_token = auth_utils.create_access_token(user.id, session_id=session.id, expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = auth_utils.create_refresh_token(user.id, session_id=session.id, expires_days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Refresh 토큰 해시 저장
    hashed_refresh = auth_utils.hash_password(refresh_token)
    session.refresh_token_hash = hashed_refresh
    db.commit()
    
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

# ----------------------------
# 내 정보 조회
# ----------------------------
@router.get("/me", response_model=UserRead)
def read_me(current_user: UserModel = Depends(auth_utils.get_current_user)) -> Any:
    return current_user

# ----------------------------
# 프로필 수정
# ----------------------------
@router.put("/profile", response_model=UserRead)
def update_profile(
    update_in: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth_utils.get_current_user),
) -> Any:
    # username 중복 확인
    if update_in.username:
        existing_user = db.query(UserModel).filter(
            UserModel.username == update_in.username,
            UserModel.id != current_user.id # 자기 자신 제외
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        current_user.username = update_in.username
    
    # email 중복 확인
    if update_in.email:
        existing_email = db.query(UserModel).filter(
            UserModel.email == update_in.email,
            UserModel.id != current_user.id # 자기 자신 제외
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")
        current_user.email = update_in.email
        
    if update_in.bio:
        current_user.bio = update_in.bio
    
    db.commit()
    db.refresh(current_user)
    return current_user

# ----------------------------
# 비밀번호 변경
# ----------------------------
@router.put("/password")
def change_password(
    pw_in: PasswordChange,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth_utils.get_current_user),
):
    if not auth_utils.verify_password(pw_in.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    
    current_user.password_hash = auth_utils.hash_password(pw_in.new_password)
    db.commit()
    return {"detail": "Password updated successfully"}

# ----------------------------
# 로그아웃 (현재 사용자의 모든 세션 삭제)
# ----------------------------
@router.post("/logout")
def logout(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth_utils.get_current_user),
):
    # 현재 사용자의 모든 세션 조회
    user_sessions = db.query(SessionModel).filter(SessionModel.user_id == current_user.id).all()

    if not user_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active sessions found for this user"
        )

    # 세션 전부 삭제
    for session in user_sessions:
        db.delete(session)

    db.commit()

    return {"detail": f"All sessions for user '{current_user.username}' have been logged out."}
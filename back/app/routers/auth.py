from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import user as user_schema
from ..models import user as user_model
from ..core.database import get_db

# 🚨 반드시 필요합니다: 비밀번호 해싱 및 JWT 관련 핵심 로직
from ..core.security import hash_password, verify_password, create_access_token 

router = APIRouter()

# --- 1. 회원가입 (Signup) ---
@router.post("/signup", response_model=user_schema.UserOut, status_code=status.HTTP_201_CREATED, tags=["Auth"])
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자를 등록하고 데이터베이스에 저장합니다.
    """
    
    # 사용자 이름 또는 이메일 중복 검사
    if db.query(user_model.UserModel).filter(
        (user_model.UserModel.username == user.username) | 
        (user_model.UserModel.email == user.email)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="사용자 이름 또는 이메일이 이미 등록되어 있습니다."
        )

    # 비밀번호 해싱
    hashed_password = hash_password(user.password)

    # DB 모델 생성
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

# --- 2. 로그인 (Login) ---
# 로그인은 토큰을 반환하므로 별도의 응답 스키마가 필요합니다.
class Token(user_schema.BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: user_schema.UserOut # 토큰과 함께 사용자 정보 반환

@router.post("/login", response_model=Token, tags=["Auth"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # username과 password를 form-data로 받습니다.
    db: Session = Depends(get_db)
):
    """
    사용자 자격 증명을 확인하고 액세스 토큰을 발급합니다.
    """
    
    # 사용자 이메일(폼 데이터에서는 username 필드를 사용)로 DB에서 사용자 찾기
    user = db.query(user_model.UserModel).filter(
        user_model.UserModel.email == form_data.username # OAuth2는 username 필드를 사용합니다.
    ).first()

    # 사용자 존재 여부 및 비밀번호 확인
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.email})
    
    # 토큰과 사용자 정보를 함께 반환
    return Token(
        access_token=access_token,
        user=user # UserOut 스키마가 ORM 모드로 사용자 모델을 자동 변환
    )
# back/app/models/user.py 파일 전체 내용 (순환 참조 방지 확인)

from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from ..core.database import Base 

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    bio = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 관계 정의 시, PostModel이 아직 정의되지 않았다면 문자열로 지정하는 것이 안전합니다.
    # 이 부분은 SQLAlchemy가 처리하므로 그대로 둡니다.
    posts = relationship("PostModel", back_populates="owner") 
    
    def __repr__(self):
        return f"<UserModel(username='{self.username}', email='{self.email}')>"
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 필요 시 추가

    uploader = relationship("User", back_populates="uploads")
    post = relationship("Post", back_populates="uploads")
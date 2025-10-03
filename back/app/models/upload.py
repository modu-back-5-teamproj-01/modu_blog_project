import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    file_path = Column(String)
    file_name = Column(String)
    content_type = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)

    uploader = relationship("User", back_populates="uploads")
    post = relationship("Post", back_populates="uploads")
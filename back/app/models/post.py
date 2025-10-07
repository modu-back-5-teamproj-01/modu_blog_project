import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    published_at = Column(DateTime)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("PostTag", back_populates="post")
    uploads = relationship("Upload", back_populates="post")
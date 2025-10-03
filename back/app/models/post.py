import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    content = Column(String)
    summary = Column(String)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    published_at = Column(DateTime)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    tags = relationship("PostTag", back_populates="post")
    uploads = relationship("Upload", back_populates="post")
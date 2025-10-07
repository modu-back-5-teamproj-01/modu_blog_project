from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship


from .base import Base
from .user import User
from .post import Post

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent_comment = relationship("Comment", remote_side=[id])
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    # parent_comment = relationship("Comment", remote_side=[id])
    # 자기 자신과의 관계 (부모 ↔ 자식 댓글)
    replies = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
        single_parent=True,
        uselist=True
    )
    
    parent = relationship(
        "Comment",
        back_populates="replies",
        remote_side=[id]        
    )
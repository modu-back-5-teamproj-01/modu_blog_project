from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class PostTag(Base):
    __tablename__ = "post_tags"
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    post = relationship("Post", back_populates="tags")
    tag = relationship("Tag", back_populates="posts")

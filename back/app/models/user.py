import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True)
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    sessions = relationship("Session", back_populates="user")
    uploads = relationship("Upload", back_populates="uploader")
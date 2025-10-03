from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship("PostTag", back_populates="tag")
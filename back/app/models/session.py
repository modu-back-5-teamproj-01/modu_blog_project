from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    refresh_token_hash = Column(String, nullable=False)
    issued_at = Column(DateTime, nullable=False, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="sessions", uselist=False)  
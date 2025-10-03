import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token_hash = Column(String)
    issued_at = Column(DateTime, default=datetime.datetime.now)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="sessions")
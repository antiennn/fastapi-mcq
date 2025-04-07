from sqlalchemy import Column, Integer, String, TIMESTAMP, text

from database import Base


class Gemini(Base):
    __tablename__ = "gemini"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, nullable=False)
    description = Column(String, nullable=True)
    last_expired_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )
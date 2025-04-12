from sqlalchemy import Column, Integer, String, ForeignKey, text, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Choice(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True)
    is_best_choice = Column(Boolean, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"),
                         nullable=False)
    question = relationship("Question", back_populates="choices")

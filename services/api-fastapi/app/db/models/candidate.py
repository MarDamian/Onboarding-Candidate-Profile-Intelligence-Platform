from sqlalchemy import String, Text, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
from datetime import datetime

class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(100))

    headline: Mapped[str] = mapped_column(String(100))
    summary: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(100))
    experience: Mapped[str] = mapped_column(Text)
    skills: Mapped[str] = mapped_column(Text)
    education: Mapped[str] = mapped_column(Text)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_indexed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
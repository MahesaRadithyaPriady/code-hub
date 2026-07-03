from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Boolean, Text, Table, Column, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

user_techs = Table(
    "user_techs",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("tech_id", ForeignKey("techs.id", ondelete="CASCADE"), primary_key=True),
)


class Tech(Base):
    __tablename__ = "techs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nama_tech: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

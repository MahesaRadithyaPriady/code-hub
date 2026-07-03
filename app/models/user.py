from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Text, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.community import user_communities
from app.models.tech import user_techs


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("roles.id"), nullable=True
    )
    photo_profile: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    provider: Mapped[str] = mapped_column(String(50), default="local")
    provider_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    techs = relationship("Tech", secondary=user_techs, lazy="selectin")
    communities = relationship("Community", secondary=user_communities, lazy="selectin")
    role = relationship("Role", lazy="selectin")

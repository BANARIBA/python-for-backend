from __future__ import annotations

from uuid import UUID, uuid4
from datetime import datetime

from typing import List, TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.posts.models import Post

class Author(Base):
    __tablename__ = "authors"
    
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=None,
        nullable=True
    )
    
    # n:1 with posts
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    
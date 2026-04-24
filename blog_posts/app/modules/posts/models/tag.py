from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime

from typing import List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.database import Base

if TYPE_CHECKING:
    from app.modules.posts.models import Post, post_tags

class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=None,
        nullable=True
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )
    
    # n:m with posts
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        secondary="post_tags",
        back_populates="tags"
    )
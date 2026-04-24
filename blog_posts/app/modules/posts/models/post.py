from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime

from typing import List, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped,mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.authors.models import Author
    from app.modules.posts.models import Tag


post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    content: Mapped[str] = mapped_column(Text, nullable=True, default='')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=None
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=None
    )
    
    # 1:n with authors
    author_id: Mapped[UUID] = mapped_column(ForeignKey("authors.id"), nullable=False)
    author: Mapped["Author"] = relationship("Author", back_populates="posts")
    
    # n:m with tags
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary="post_tags",
        back_populates="posts"
    )
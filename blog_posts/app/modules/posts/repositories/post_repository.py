from datetime import datetime, timezone, time
from uuid import UUID

from sqlalchemy.orm import Session

from sqlalchemy.orm import joinedload
from sqlalchemy import select, func

from app.modules.posts.schemas import FindPostsDto, CreatePostDto
from app.modules.posts.models import Post
from app.modules.authors.models import Author

class PostRepository():
    def __init__(self, get_db_connection: Session) -> None:
        self.get_db_connection = get_db_connection
        
    def find_all_by(self, find_post_dto: FindPostsDto):
        stmt = select(Post).options(joinedload(Post.author))
        count_stmt = select(func.count()).select_from(Post)
        
        filters = []
        
        if find_post_dto.title:
            filters.append(Post.title.ilike(f"%{find_post_dto.title}%"))
            
        if find_post_dto.content:
            filters.append(Post.content.ilike(f"%{find_post_dto.content}%"))
            
        if find_post_dto.author:
            filters.append(Post.author_id==find_post_dto.author)
            
        if find_post_dto.is_active is not None:
            filters.append(Post.is_active==find_post_dto.is_active)
            
        if find_post_dto.init_created_date:
            now = datetime.combine(find_post_dto.init_created_date, time.min, timezone.utc)
            filters.append(Post.created_at >= now)
        
        if find_post_dto.end_created_date:
            end = datetime.combine(find_post_dto.end_created_date, time.min, timezone.utc)
            filters.append(Post.created_at <= end)
            
        if filters:
            stmt = stmt.where(*filters)
            count_stmt = count_stmt.where(*filters)
            
        offset = (find_post_dto.page - 1) * find_post_dto.limit
        
        stmt = (
            stmt
                .order_by(Post.created_at.desc())
                .limit(find_post_dto.limit)
                .offset(offset)
        )

        data = self.get_db_connection.execute(stmt).scalars().all()
        total = self.get_db_connection.execute(count_stmt).scalar_one()
            
        return {
            "data": data,
            "meta": {
                "page": find_post_dto.page,
                "limit": find_post_dto.limit,
                "total": total,
                "total_pages": (total + find_post_dto.limit - 1) // find_post_dto.limit
            },
        }
            
        
    
    def find_one_by(self, id) -> Post | None:
        stmt = (
            select(Post)
            .options(joinedload(Post.author))
            .where(Post.id == id)
        )
        return (
            self
                .get_db_connection
                .execute(stmt)
                .scalar_one_or_none()
        )
    
    def create(self, create_post_dto: CreatePostDto, author: Author) -> Post:
        new_post = Post(
            title=create_post_dto.title,
            content=create_post_dto.content,
            author=author
        )
        self.get_db_connection.add(new_post)
        self.get_db_connection.commit()
        self.get_db_connection.refresh(new_post)
        return new_post
    
    def update(self, post: Post, update_fields: dict) -> Post:
        now = datetime.now(timezone.utc)
        for key, value in update_fields.items():
            setattr(post, key, value)
        setattr(post, 'updated_at', now)
        self.get_db_connection.add(post)
        self.get_db_connection.commit()
        self.get_db_connection.refresh(post)
        return post        
    
    def delete(self, post: Post) -> Post:
        now = datetime.now(timezone.utc)
        setattr(post, 'deleted_at', now)
        setattr(post, 'updated_at', now)
        setattr(post, 'is_active', False)
        self.get_db_connection.add(post)
        self.get_db_connection.commit()
        self.get_db_connection.refresh(post)
        return post
    
    def reactivate(self, post: Post) -> Post:
        now = datetime.now(timezone.utc)
        setattr(post, 'deleted_at', None)
        setattr(post, 'updated_at', now)
        setattr(post, 'is_active', True)
        self.get_db_connection.add(post)
        self.get_db_connection.commit()
        self.get_db_connection.refresh(post)
        return post
    
from uuid import UUID
from datetime import datetime, time, timezone

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.modules.authors.schemas import FindAuthorsDto, CreateAuthorDto
from app.modules.authors.models import Author

class AuthorRepository:
    def __init__(self, get_db_connection: Session) -> None:
        self.get_db_connection = get_db_connection
        
    def find_all_by(self, find_author_dto: FindAuthorsDto):
        stmt = select(Author)
        count_stmt = select(func.count()).select_from(Author)
        
        if find_author_dto.name:
            stmt = stmt.where(Author.name.ilike(f'%{find_author_dto.name}%'))
            count_stmt = count_stmt.where(Author.name.ilike(f'%{find_author_dto.name}%'))

        if find_author_dto.email:
            stmt = stmt.where(Author.email.ilike(f'%{find_author_dto.email}%'))
            count_stmt = count_stmt.where(Author.email.ilike(f'%{find_author_dto.email}%'))
        
        if find_author_dto.is_active is not None:
            stmt = stmt.where(Author.is_active == find_author_dto.is_active)
            count_stmt = count_stmt.where(Author.is_active == find_author_dto.is_active)
            
        if find_author_dto.init_created_date:
            init_datetime = datetime.combine(find_author_dto.init_created_date, time.min, tzinfo=timezone.utc)
            stmt = stmt.where(Author.created_at >= init_datetime)
            count_stmt = count_stmt.where(Author.created_at >= init_datetime)
        
        if find_author_dto.end_created_date:
            end_datetime = datetime.combine(find_author_dto.end_created_date, time.min, timezone.utc)
            stmt = stmt.where(Author.created_at <= end_datetime)
            count_stmt = count_stmt.where(Author.created_at <= end_datetime)
        
        offset = (find_author_dto.page - 1) * find_author_dto.limit
        stmt = stmt.order_by(Author.created_at.desc()).limit(find_author_dto.limit).offset(offset)
        
        data = self.get_db_connection.execute(stmt).scalars().all()
        total = self.get_db_connection.execute(count_stmt).scalar_one()
        
        return {
            "data": data,
            "meta": {
                "page": find_author_dto.page,
                "limit": find_author_dto.limit,
                "total": total,
                "total_pages": (total + find_author_dto.limit - 1) // find_author_dto.limit
            }
        }
            
    
    def find_one_by(self, id: UUID) -> Author | None:
        stmt = select(Author).where(Author.id==id)
        return self.get_db_connection.execute(stmt).scalar_one_or_none()
        
    
    def create(self, createAuthorDto: CreateAuthorDto) -> Author:
        author = Author(
            name=createAuthorDto.name,
            email=createAuthorDto.email
        )
        self.get_db_connection.add(author)
        self.get_db_connection.commit()
        self.get_db_connection.refresh(author)
        return author
    
    def update(self, author: Author, update_field: dict):
        now = datetime.now(timezone.utc)
        for key, value in update_field.items():
            setattr(author, key, value)
        setattr(author, 'updated_at', now)
        self.get_db_connection.add(author)
        self.get_db_connection.commit()
        self.get_db_connection.refresh(author)
        return author
    
    def delete(self, author: Author):
        now = datetime.now(timezone.utc)
        setattr(author, 'is_active', False)
        setattr(author, 'deleted_at', now)
        setattr(author, 'updated_at', now)
        self.get_db_connection.add(author)
        self.get_db_connection.commit()
        self.get_db_connection.refresh(author)
        return author
    
    def reactivate(self, author: Author):
        now = datetime.now(timezone.utc)
        setattr(author, 'is_active', True)
        setattr(author, 'deleted_at', None)
        setattr(author, 'updated_at', now)
        self.get_db_connection.add(author)
        self.get_db_connection.commit()
        self.get_db_connection.refresh(author)
        return author
    
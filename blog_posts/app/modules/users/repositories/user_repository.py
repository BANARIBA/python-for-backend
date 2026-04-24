from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from sqlalchemy import select, func

from app.modules.users.models import User
from app.modules.users.schemas import FindUsersDto

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all_by(self, dto: FindUsersDto):
        stmt = select(User)
        count_stmt = select(func.count()).select_from(User)
        filters = []

        if dto.complete_name:
            filters.append(User.complete_name.ilike(f"%{dto.complete_name}%"))
        if dto.email:
            filters.append(User.email.ilike(f"%{dto.email}%"))
        if dto.is_active is not None:
            filters.append(User.is_active == dto.is_active)

        if filters:
            stmt = stmt.where(*filters)
            count_stmt = count_stmt.where(*filters)

        offset = (dto.page - 1) * dto.limit
        stmt = stmt.order_by(User.created_at.desc()).limit(dto.limit).offset(offset)

        data = self.db.execute(stmt).scalars().all()
        total = self.db.execute(count_stmt).scalar_one()
        return {"data": data, "total": total}

    def find_one_by(self, id: UUID):
        return self.db.execute(select(User).where(User.id == id)).scalar_one_or_none()

    def find_by_email(self, email: str):
        return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, fields: dict):
        for key, value in fields.items():
            setattr(user, key, value)
        user.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User):
        user.is_active = False
        user.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
        return user
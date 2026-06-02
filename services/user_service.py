from sqlalchemy.orm import Session
from models.user import User
from repositories.generic_repository import GenericRepository
from schemas.user_schema import UserCreate, UserUpdate
from typing import List, Optional

# Instantiate the generic repository with the User model
user_repo = GenericRepository(model=User)

def get_all_users(db: Session) -> List[User]:
    return user_repo.get_all(db)

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return user_repo.get_by_id(db, user_id)

def create_user(db: Session, user_data: UserCreate) -> User:
    return user_repo.create(db, user_data.model_dump())

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    # Only update fields that are provided
    update_data = user_data.model_dump(exclude_unset=True)
    return user_repo.update(db, user_id, update_data)

def delete_user(db: Session, user_id: int) -> bool:
    return user_repo.delete(db, user_id)

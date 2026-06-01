from repositories.generic_repository import GenericRepository
from schemas.user_schema import UserCreate, UserUpdate
from typing import List, Dict, Optional, Any

# Instantiate the generic repository for the "users" table
user_repo = GenericRepository(table_name="users")

def get_all_users() -> List[Dict[str, Any]]:
    return user_repo.get_all()

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    return user_repo.get_by_id(user_id)

def create_user(user_data: UserCreate) -> Dict[str, Any]:
    return user_repo.create(user_data.model_dump())

def update_user(user_id: int, user_data: UserUpdate) -> Optional[Dict[str, Any]]:
    # Only update fields that are provided
    update_data = user_data.model_dump(exclude_unset=True)
    return user_repo.update(user_id, update_data)

def delete_user(user_id: int) -> bool:
    return user_repo.delete(user_id)

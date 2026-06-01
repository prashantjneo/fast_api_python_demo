from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
import services.user_service as user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=List[UserResponse])
def get_users():
    return user_service.get_all_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    return user_service.create_user(user)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    updated_user = user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

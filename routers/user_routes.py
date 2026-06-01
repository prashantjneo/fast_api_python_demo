from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from schemas.response_schema import APIResponse
from utils.response import success_response
import services.user_service as user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=APIResponse[List[UserResponse]])
def get_users():
    return success_response(data=user_service.get_all_users(), message="Users fetched successfully")

@router.get("/{user_id}", response_model=APIResponse[UserResponse])
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(data=user, message="User fetched successfully")

@router.post("/", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    return success_response(data=user_service.create_user(user), message="User created successfully", code=status.HTTP_201_CREATED)

@router.put("/{user_id}", response_model=APIResponse[UserResponse])
def update_user(user_id: int, user: UserUpdate):
    updated_user = user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(data=updated_user, message="User updated successfully")

@router.delete("/{user_id}", response_model=APIResponse)
def delete_user(user_id: int):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(message="User deleted successfully")

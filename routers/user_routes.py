from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from schemas.response_schema import APIResponse
from utils.response import success_response
from database.connection import get_db
from utils.dependencies import get_current_user
import services.user_service as user_service
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=APIResponse[List[UserResponse]])
def get_users(db: Session = Depends(get_db)):
    return success_response(data=user_service.get_all_users(db), message="Users fetched successfully")

@router.get("/profile", response_model=APIResponse[UserResponse])
def get_profile(current_user: User = Depends(get_current_user)):
    return success_response(data=current_user, message="User profile fetched successfully")

@router.get("/{user_id}", response_model=APIResponse[UserResponse])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(data=user, message="User fetched successfully")

@router.post("/", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return success_response(data=user_service.create_user(db, user), message="User created successfully", code=status.HTTP_201_CREATED)

@router.put("/{user_id}", response_model=APIResponse[UserResponse])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_service.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(data=updated_user, message="User updated successfully")

@router.delete("/{user_id}", response_model=APIResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(message="User deleted successfully")

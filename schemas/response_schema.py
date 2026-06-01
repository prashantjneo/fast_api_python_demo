from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any, List

T = TypeVar('T')

class ErrorDetail(BaseModel):
    field: str
    message: str

class APIResponse(BaseModel, Generic[T]):
    success: bool
    code: int
    message: str
    data: Optional[T] = None
    errors: Optional[List[ErrorDetail]] = None

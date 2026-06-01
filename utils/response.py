from typing import Any, Optional

def success_response(data: Any = None, message: str = "Data fetched successfully", code: int = 200) -> dict:
    """
    Utility function to format success responses globally.
    """
    return {
        "success": True,
        "code": code,
        "message": message,
        "data": data,
        "errors": None
    }

def error_response(message: str = "An error occurred", code: int = 400, errors: Optional[list] = None) -> dict:
    """
    Utility function to format error responses globally.
    """
    return {
        "success": False,
        "code": code,
        "message": message,
        "data": None,
        "errors": errors
    }

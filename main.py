from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.response import error_response
from routers import user_routes
from routers import auth_routes
from database.connection import engine, Base
import models.user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = "->".join([str(loc) for loc in error["loc"][1:]]) if len(error["loc"]) > 1 else str(error["loc"][0])
        errors.append({"field": field, "message": error["msg"]})
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response(message="Validation Failed", code=400, errors=errors)
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=str(exc.detail), code=exc.status_code)
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content=error_response(message="Internal Server Error", code=500)
    )

app.include_router(user_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to FastAPI"
    }
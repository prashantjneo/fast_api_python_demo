from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.auth_schema import LoginRequest, SignupRequest, VerifyOTPRequest, Token, SendOTPRequest, RefreshTokenRequest
from schemas.response_schema import APIResponse
from utils.response import success_response
import services.auth_service as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=APIResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user = auth_service.signup_user(db, request)
    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return success_response(message="User registered successfully. Check your console for the OTP.", code=status.HTTP_201_CREATED)

@router.post("/send-otp", response_model=APIResponse)
def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    success = auth_service.send_otp(db, request.email)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(message="OTP sent successfully. Check your console.")

@router.post("/verify-otp", response_model=APIResponse)
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    success = auth_service.verify_otp(db, request.email, request.otp)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid OTP or user not found")
    return success_response(message="Email verified successfully. You can now login.")

@router.post("/login", response_model=APIResponse[Token])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    result = auth_service.authenticate_user(db, request)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if result == "not_verified":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified. Please verify OTP first.")
    
    return success_response(data=result, message="Login successful")

@router.post("/refresh", response_model=APIResponse[Token])
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    result = auth_service.refresh_access_token(db, request.refresh_token)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    
    return success_response(data=result, message="Token refreshed successfully")

@router.post("/logout", response_model=APIResponse)
def logout(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    success = auth_service.logout_user(db, request.refresh_token)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    return success_response(message="Logged out successfully")

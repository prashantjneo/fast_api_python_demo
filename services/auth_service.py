import random
import string
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import User
from schemas.auth_schema import SignupRequest, LoginRequest, SendOTPRequest
from datetime import datetime, timedelta
from jose import jwt
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_otp(length=6):
    # Returning a hardcoded OTP for easy testing since we have no real email
    return "54321"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def signup_user(db: Session, request: SignupRequest):
    # Check if user exists
    db_user = db.query(User).filter(User.email == request.email).first()
    if db_user:
        return None

    hashed_pwd = get_password_hash(request.password)
    otp = generate_otp()
    
    new_user = User(
        name=request.name,
        email=request.email,
        hashed_password=hashed_pwd,
        otp_code=otp,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # MOCK SENDING OTP
    print("="*40)
    print(f"MOCK EMAIL: Sending OTP to {new_user.email}")
    print(f"Your OTP Code is: {otp}")
    print("="*40)
    
    return new_user

def send_otp(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return False
        
    otp = generate_otp()
    db_user.otp_code = otp
    db.commit()
    
    # MOCK SENDING OTP
    print("="*40)
    print(f"MOCK EMAIL: Re-sending OTP to {email}")
    print(f"Your new OTP Code is: {otp}")
    print("="*40)
    
    return True

def verify_otp(db: Session, email: str, otp: str):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return False
    
    if db_user.otp_code == otp:
        db_user.is_verified = True
        db_user.otp_code = None # clear OTP after success
        db.commit()
        return True
    return False

def authenticate_user(db: Session, request: LoginRequest):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        return None
    if not verify_password(request.password, db_user.hashed_password):
        return None
    if not db_user.is_verified:
        return "not_verified"
        
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

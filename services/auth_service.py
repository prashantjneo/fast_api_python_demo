import random
import string
import bcrypt
from sqlalchemy.orm import Session
from models.user import User
from models.refresh_token import RefreshToken
from schemas.auth_schema import SignupRequest, LoginRequest, SendOTPRequest
from datetime import datetime, timedelta
from jose import jwt, JWTError
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    try:
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except ValueError:
        return False

def generate_otp(length=6):
    # Returning a hardcoded OTP for easy testing since we have no real email
    return "54321"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    # FOR DEMO PURPOSE: Reduce refresh token time to 2 minutes
    expire = datetime.utcnow() + timedelta(minutes=2)
    to_encode.update({"exp": expire, "type": "refresh"})
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
    refresh_token_str = create_refresh_token(data={"sub": db_user.email})
    
    # expire_date = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    # FOR DEMO PURPOSE: Reduce refresh token time to 2 minutes
    expire_date = datetime.utcnow() + timedelta(minutes=2)
    db_refresh_token = RefreshToken(
        token=refresh_token_str,
        user_id=db_user.id,
        expires_at=expire_date
    )
    db.add(db_refresh_token)
    db.commit()
    
    return {"access_token": access_token, "refresh_token": refresh_token_str, "token_type": "bearer"}

def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if email is None or token_type != "refresh":
            return None
            
        db_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if not db_token or db_token.revoked or db_token.expires_at < datetime.utcnow():
            return None
            
        db_user = db.query(User).filter(User.id == db_token.user_id).first()
        if not db_user:
            return None
            
        access_token = create_access_token(data={"sub": db_user.email})
        new_refresh_token_str = create_refresh_token(data={"sub": db_user.email})
        
        db.delete(db_token)
        # new_expire_date = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        # FOR DEMO PURPOSE: Reduce refresh token time to 2 minutes
        new_expire_date = datetime.utcnow() + timedelta(minutes=2)
        new_db_token = RefreshToken(
            token=new_refresh_token_str,
            user_id=db_user.id,
            expires_at=new_expire_date
        )
        db.add(new_db_token)
        db.commit()
        
        return {"access_token": access_token, "refresh_token": new_refresh_token_str, "token_type": "bearer"}
    except JWTError:
        return None

def logout_user(db: Session, refresh_token: str):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if db_token:
        # Option A: Global Logout - revoke all tokens for this user
        user_id = db_token.user_id
        db.query(RefreshToken).filter(RefreshToken.user_id == user_id).update({"revoked": True})
        db.commit()
        return True
    return False

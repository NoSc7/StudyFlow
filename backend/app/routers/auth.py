"""Authentication endpoints"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.security import hash_password, verify_password, create_access_token
from app.config import settings

router = APIRouter()


class LoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class RegisterRequest:
    def __init__(self, email: str, username: str, password: str):
        self.email = email
        self.username = username
        self.password = password


@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    user = db.query(User).filter(
        (User.email == request.email) | (User.username == request.username)
    ).first()
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered",
        )
    
    # Create new user
    new_user = User(
        email=request.email,
        username=request.username,
        hashed_password=hash_password(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"id": new_user.id, "email": new_user.email, "username": new_user.username}


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(db: Session = Depends(get_db)):
    """Get current user profile"""
    # Implementation depends on auth flow
    pass

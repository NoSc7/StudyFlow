"""Dependency injection utilities"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.security import verify_token


async def get_current_user(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return token

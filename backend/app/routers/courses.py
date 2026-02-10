"""Courses endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Course, User
from app.deps import get_current_user

router = APIRouter()


@router.get("/")
async def list_courses(db: Session = Depends(get_db)):
    """List all courses"""
    courses = db.query(Course).all()
    return courses


@router.post("/")
async def create_course(
    title: str,
    description: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new course"""
    user_id = current_user.get("sub")
    new_course = Course(
        title=title,
        description=description,
        owner_id=int(user_id),
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@router.get("/{course_id}")
async def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a specific course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.put("/{course_id}")
async def update_course(
    course_id: int,
    title: str,
    description: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if course.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    course.title = title
    course.description = description
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a course"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if course.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted"}

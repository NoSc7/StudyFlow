"""Modules endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Module, Course
from app.deps import get_current_user

router = APIRouter()


@router.get("/course/{course_id}")
async def list_modules(course_id: int, db: Session = Depends(get_db)):
    """List modules for a course"""
    modules = db.query(Module).filter(Module.course_id == course_id).order_by(Module.order).all()
    return modules


@router.post("/")
async def create_module(
    course_id: int,
    title: str,
    description: str,
    order: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new module"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if course.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    new_module = Module(
        title=title,
        description=description,
        course_id=course_id,
        order=order,
    )
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return new_module


@router.get("/{module_id}")
async def get_module(module_id: int, db: Session = Depends(get_db)):
    """Get a specific module"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    return module


@router.put("/{module_id}")
async def update_module(
    module_id: int,
    title: str,
    description: str,
    order: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a module"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    
    course = db.query(Course).filter(Course.id == module.course_id).first()
    if course.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    module.title = title
    module.description = description
    module.order = order
    db.commit()
    db.refresh(module)
    return module


@router.delete("/{module_id}")
async def delete_module(
    module_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a module"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    
    course = db.query(Course).filter(Course.id == module.course_id).first()
    if course.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db.delete(module)
    db.commit()
    return {"message": "Module deleted"}

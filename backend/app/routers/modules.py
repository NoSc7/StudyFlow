"""Modules endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Module, Course
from app.deps import get_current_user
from app.schemas import ModuleCreate, Module as ModuleSchema

router = APIRouter()


@router.get("/course/{course_id}", response_model=list[ModuleSchema])
async def list_modules(course_id: int, db: Session = Depends(get_db)):
    """List modules for a course"""
    modules = db.query(Module).filter(Module.course_id == course_id).order_by(Module.order).all()
    return modules


@router.post("/", response_model=ModuleSchema)
async def create_module(
    module: ModuleCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new module"""
    course = db.query(Course).filter(Course.id == module.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if course.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    new_module = Module(
        title=module.title,
        description=module.description,
        course_id=module.course_id,
        order=module.order,
    )
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return new_module


@router.get("/{module_id}", response_model=ModuleSchema)
async def get_module(module_id: int, db: Session = Depends(get_db)):
    """Get a specific module"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    return module


@router.put("/{module_id}", response_model=ModuleSchema)
async def update_module(
    module_id: int,
    module: ModuleCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a module"""
    db_module = db.query(Module).filter(Module.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    
    course = db.query(Course).filter(Course.id == db_module.course_id).first()
    if course.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db_module.title = module.title
    db_module.description = module.description
    db_module.order = module.order
    db.commit()
    db.refresh(db_module)
    return db_module


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

"""Tasks endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Task, Module
from app.deps import get_current_user

router = APIRouter()


@router.get("/module/{module_id}")
async def list_tasks(module_id: int, db: Session = Depends(get_db)):
    """List tasks for a module"""
    tasks = db.query(Task).filter(Task.module_id == module_id).all()
    return tasks


@router.post("/")
async def create_task(
    module_id: int,
    title: str,
    description: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    
    new_task = Task(
        title=title,
        description=description,
        module_id=module_id,
        owner_id=int(current_user.get("sub")),
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}")
async def update_task(
    task_id: int,
    title: str,
    description: str,
    is_completed: bool = False,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    task.title = title
    task.description = description
    task.is_completed = is_completed
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

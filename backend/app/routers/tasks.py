"""Tasks endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Task, Module
from app.deps import get_current_user
from app.schemas import TaskCreate, Task as TaskSchema

router = APIRouter()


@router.get("/module/{module_id}", response_model=list[TaskSchema])
async def list_tasks(module_id: int, db: Session = Depends(get_db)):
    """List tasks for a module"""
    tasks = db.query(Task).filter(Task.module_id == module_id).all()
    return tasks


@router.post("/", response_model=TaskSchema)
async def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task"""
    module = db.query(Module).filter(Module.id == task.module_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    
    new_task = Task(
        title=task.title,
        description=task.description,
        module_id=task.module_id,
        owner_id=int(current_user.get("sub")),
        is_completed=task.is_completed,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if db_task.owner_id != int(current_user.get("sub")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    db_task.title = task.title
    db_task.description = task.description
    db_task.is_completed = task.is_completed
    db.commit()
    db.refresh(db_task)
    return db_task


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

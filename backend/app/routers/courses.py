from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models import Course
from pydantic import BaseModel

router = APIRouter()


# ====== Schemas simples ======

class CourseCreate(BaseModel):
    title: str
    description: str | None = None


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str | None

    class Config:
        from_attributes = True


# ====== Routes ======

@router.get("/", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(
        title=course.title,
        description=course.description,
        owner_id=1  # TEMPORAIRE (auth plus tard)
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

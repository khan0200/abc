from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import secrets

from backend.app.database import get_db
from backend.app.models.course import Course

router = APIRouter(prefix="/courses", tags=["Courses"])

class CourseCreate(BaseModel):
    name: str
    level: str
    price: float
    currency: Optional[str] = "$"
    description: Optional[str] = None
    is_active: Optional[bool] = True

class CourseOut(CourseCreate):
    id: str

@router.get("", response_model=List[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    """Retrieve all available courses configured in Settings."""
    return [
        CourseOut(
            id=c.id,
            name=c.name,
            level=c.level,
            price=c.price,
            currency=c.currency or "$",
            description=c.description,
            is_active=c.is_active
        )
        for c in db.query(Course).all()
    ]

@router.post("", response_model=CourseOut)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course in Settings."""
    existing = db.query(Course).filter(Course.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course name already exists.")

    course = Course(
        id=f"course-{secrets.token_hex(4)}",
        name=data.name,
        level=data.level,
        price=data.price,
        currency=data.currency or "$",
        description=data.description,
        is_active=data.is_active
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return CourseOut(
        id=course.id,
        name=course.name,
        level=course.level,
        price=course.price,
        currency=course.currency or "$",
        description=course.description,
        is_active=course.is_active
    )

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import secrets

from backend.app.database import get_db
from backend.app.models.user import User, UserRole, RoleCategory
from backend.app.schemas.user import LoginRequest, LoginResponse, UserOut
from backend.app.core.security import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication & Roles"])

@router.get("/roles")
def get_platform_roles() -> Dict[str, Any]:
    """Return all platform roles organized by category hierarchy."""
    return {
        "education_center": {
            "category": "Education center (Staff / Operations)",
            "roles": [
                {
                    "key": UserRole.DIRECTOR.value,
                    "title": "Director",
                    "description": "Executive authority with complete administrative and financial access across all branches."
                },
                {
                    "key": UserRole.BRANCH_DIRECTOR.value,
                    "title": "Branch Director",
                    "description": "Branch supervisor overseeing staff, classroom facilities, and local student cohorts."
                },
                {
                    "key": UserRole.TEACHER.value,
                    "title": "Teacher",
                    "description": "Instructor responsible for teaching classes, managing student attendance, and entering grades."
                },
                {
                    "key": UserRole.MANAGER.value,
                    "title": "Manager",
                    "description": "Operational manager handling leads, student admissions, schedule planning, and billing inquiries."
                }
            ]
        },
        "student": {
            "category": "Student Portal",
            "roles": [
                {
                    "key": UserRole.STUDENT.value,
                    "title": "Student",
                    "description": "Learner portal for viewing class schedules, coursework, learning materials, and academic attendance."
                }
            ]
        },
        "parent": {
            "category": "Parents Portal",
            "roles": [
                {
                    "key": UserRole.PARENT.value,
                    "title": "Parents",
                    "description": "Guardian portal for monitoring children's progress, teacher remarks, tuition invoices, and receipts."
                }
            ]
        }
    }

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    """List all accounts and their platform roles."""
    return db.query(User).all()

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user by username or email and password."""
    user = db.query(User).filter(
        (User.username == data.username_or_email) | (User.email == data.username_or_email)
    ).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated."
        )

    # Generate a demo session token
    token = f"token_{user.role.value}_{secrets.token_hex(16)}"

    return LoginResponse(
        success=True,
        message=f"Welcome back, {user.full_name}!",
        user=UserOut.from_orm(user),
        token=token
    )

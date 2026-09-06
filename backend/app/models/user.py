from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from backend.app.database import Base

class RoleCategory(str, Enum):
    EDUCATION_CENTER = "education_center"
    STUDENT = "student"
    PARENT = "parent"

class UserRole(str, Enum):
    # Education center roles
    DIRECTOR = "director"
    BRANCH_DIRECTOR = "branch_director"
    TEACHER = "teacher"
    MANAGER = "manager"
    # End-user portal roles
    STUDENT = "student"
    PARENT = "parent"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, index=True)
    category = Column(SQLEnum(RoleCategory), nullable=False)
    branch = Column(String, nullable=True) # E.g. "Main Campus", "Downtown Branch"
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role.value,
            "category": self.category.value,
            "branch": self.branch,
            "phone": self.phone,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

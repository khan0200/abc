from pydantic import BaseModel, EmailStr
from typing import Optional
from backend.app.models.user import UserRole, RoleCategory

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: UserRole
    category: RoleCategory
    branch: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserOut] = None
    token: Optional[str] = None

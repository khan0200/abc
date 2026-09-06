from backend.app.database import engine, SessionLocal, Base
from backend.app.models.user import User, UserRole, RoleCategory
from backend.app.core.security import get_password_hash

DEMO_USERS = [
    {
        "username": "director",
        "email": "director@educrm.com",
        "password": "Director@2026",
        "full_name": "Sarah Jenkins",
        "role": UserRole.DIRECTOR,
        "category": RoleCategory.EDUCATION_CENTER,
        "branch": "Central Campus",
        "phone": "+1 (555) 019-2831"
    },
    {
        "username": "branch_director",
        "email": "branch.director@educrm.com",
        "password": "Branch@2026",
        "full_name": "Michael Chang",
        "role": UserRole.BRANCH_DIRECTOR,
        "category": RoleCategory.EDUCATION_CENTER,
        "branch": "Downtown Branch",
        "phone": "+1 (555) 019-4582"
    },
    {
        "username": "teacher",
        "email": "teacher@educrm.com",
        "password": "Teacher@2026",
        "full_name": "Elena Rostova",
        "role": UserRole.TEACHER,
        "category": RoleCategory.EDUCATION_CENTER,
        "branch": "Central Campus",
        "phone": "+1 (555) 019-7819"
    },
    {
        "username": "manager",
        "email": "manager@educrm.com",
        "password": "Manager@2026",
        "full_name": "David Miller",
        "role": UserRole.MANAGER,
        "category": RoleCategory.EDUCATION_CENTER,
        "branch": "Central Campus",
        "phone": "+1 (555) 019-3920"
    },
    {
        "username": "student",
        "email": "student@educrm.com",
        "password": "Student@2026",
        "full_name": "Alex Johnson",
        "role": UserRole.STUDENT,
        "category": RoleCategory.STUDENT,
        "branch": "Central Campus",
        "phone": "+1 (555) 019-6102"
    },
    {
        "username": "parent",
        "email": "parent@educrm.com",
        "password": "Parent@2026",
        "full_name": "Robert & Lisa Johnson",
        "role": UserRole.PARENT,
        "category": RoleCategory.PARENT,
        "branch": "Central Campus",
        "phone": "+1 (555) 019-9401"
    }
]

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for u in DEMO_USERS:
            existing = db.query(User).filter(
                (User.username == u["username"]) | (User.email == u["email"])
            ).first()
            if not existing:
                user = User(
                    username=u["username"],
                    email=u["email"],
                    hashed_password=get_password_hash(u["password"]),
                    full_name=u["full_name"],
                    role=u["role"],
                    category=u["category"],
                    branch=u["branch"],
                    phone=u["phone"],
                    is_active=True
                )
                db.add(user)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database with platform roles...")
    init_db()
    print("Database seeded successfully!")

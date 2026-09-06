from backend.app.database import engine, SessionLocal, Base
from backend.app.models.user import User, UserRole, RoleCategory
from backend.app.models.course import Course
from backend.app.models.lead import Lead, LeadStatusEnum, ClosedReasonEnum
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

DEMO_COURSES = [
    {
        "id": "course-starter",
        "name": "Starter",
        "level": "Beginner",
        "price": 180.0,
        "description": "Foundational English vocabulary & grammar"
    },
    {
        "id": "course-elementary",
        "name": "Elementary",
        "level": "A1 - A2",
        "price": 200.0,
        "description": "Basic conversational sentence structures"
    },
    {
        "id": "course-intermediate",
        "name": "Intermediate",
        "level": "B1 - B2",
        "price": 240.0,
        "description": "Fluent conversation and practical writing"
    },
    {
        "id": "course-advanced",
        "name": "Advanced",
        "level": "C1",
        "price": 280.0,
        "description": "Academic reading, debate, and advanced grammar"
    },
    {
        "id": "course-ielts",
        "name": "IELTS Preparation",
        "level": "Exam Prep",
        "price": 320.0,
        "description": "Intensive speaking, writing, and test strategies"
    },
    {
        "id": "course-toefl",
        "name": "TOEFL iBT",
        "level": "Exam Prep",
        "price": 320.0,
        "description": "Targeted preparation for university admissions"
    },
    {
        "id": "course-korean",
        "name": "Korean Language",
        "level": "TOPIK I - II",
        "price": 220.0,
        "description": "Hangul mastery, everyday conversation & culture"
    },
    {
        "id": "course-chinese",
        "name": "Chinese (Mandarin)",
        "level": "HSK 1 - 4",
        "price": 220.0,
        "description": "Pinyin, character writing, and practical dialog"
    }
]

DEMO_LEADS = [
    {
        "id": "lead-1",
        "name": "Min-jun Kim",
        "phone": "010-3456-7890",
        "course_id": "course-ielts",
        "course_name": "IELTS Preparation",
        "status": LeadStatusEnum.COLD,
        "source": "Instagram Ad",
        "notes": "Aiming for 7.0 band score for UK master study application.",
        "preferred_time": "Evening",
        "assigned_manager": "David Miller"
    },
    {
        "id": "lead-2",
        "name": "Seo-yeon Lee",
        "phone": "010-9123-4567",
        "course_id": "course-korean",
        "course_name": "Korean Language",
        "status": LeadStatusEnum.COLD,
        "source": "Walk-in",
        "notes": "Inquired about weekend intermediate speaking class.",
        "preferred_time": "Weekend Morning",
        "assigned_manager": "Sarah Jenkins"
    },
    {
        "id": "lead-3",
        "name": "Ji-woo Park",
        "phone": "010-8765-4321",
        "course_id": "course-toefl",
        "course_name": "TOEFL iBT",
        "status": LeadStatusEnum.WAITING,
        "source": "Referral",
        "notes": "Placement consultation complete. Waiting for schedule confirmation on Tuesday/Thursday.",
        "preferred_time": "Evening",
        "assigned_manager": "David Miller"
    },
    {
        "id": "lead-4",
        "name": "Dong-hyun Choi",
        "phone": "010-0000-0000",
        "course_id": "course-advanced",
        "course_name": "Advanced",
        "status": LeadStatusEnum.CLOSED,
        "closed_reason": ClosedReasonEnum.WRONG_NUMBER,
        "source": "Website Form",
        "notes": "Phone number was disconnected or answered by another party."
    }
]

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed users
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

        # Seed courses
        for c in DEMO_COURSES:
            existing_course = db.query(Course).filter(Course.id == c["id"]).first()
            if not existing_course:
                course = Course(
                    id=c["id"],
                    name=c["name"],
                    level=c["level"],
                    price=c["price"],
                    currency="$",
                    description=c["description"],
                    is_active=True
                )
                db.add(course)

        db.commit()

        # Seed leads
        for l in DEMO_LEADS:
            existing_lead = db.query(Lead).filter(Lead.id == l["id"]).first()
            if not existing_lead:
                lead = Lead(
                    id=l["id"],
                    name=l["name"],
                    phone=l["phone"],
                    course_id=l["course_id"],
                    course_name=l["course_name"],
                    status=l["status"],
                    closed_reason=l.get("closed_reason"),
                    source=l.get("source"),
                    notes=l.get("notes"),
                    preferred_time=l.get("preferred_time"),
                    assigned_manager=l.get("assigned_manager")
                )
                db.add(lead)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database with platform roles, courses, and leads...")
    init_db()
    print("Database seeded successfully!")

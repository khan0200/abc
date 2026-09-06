from backend.app.database import engine, SessionLocal, Base
from backend.app.models.user import User, UserRole, RoleCategory
from backend.app.models.course import Course
from backend.app.models.lead import Lead, LeadStatusEnum, ClosedReasonEnum
from backend.app.models.student import Student, StudentStatusEnum, TuitionStatusEnum
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

DEMO_STUDENTS = [
    {
        "id": "student-1",
        "student_id": "STU-2026-001",
        "name": "Min-jun Kim",
        "email": "minjun.kim@student.edu",
        "phone": "010-3456-7890",
        "guardian_name": "Hyun-woo Kim",
        "guardian_phone": "010-1122-3344",
        "course_id": "course-ielts",
        "course_name": "IELTS Preparation",
        "group_name": "IELTS Morning A (Mon/Wed/Fri)",
        "branch": "Central Campus",
        "status": StudentStatusEnum.ACTIVE,
        "tuition_status": TuitionStatusEnum.PAID,
        "balance": 0.0,
        "attendance_rate": 98,
        "enrolled_at": "2026-08-15"
    },
    {
        "id": "student-2",
        "student_id": "STU-2026-002",
        "name": "Ji-woo Park",
        "email": "jiwoo.park@student.edu",
        "phone": "010-8765-4321",
        "guardian_name": "Eun-sook Choi",
        "guardian_phone": "010-5566-7788",
        "course_id": "course-toefl",
        "course_name": "TOEFL iBT",
        "group_name": "TOEFL Evening B (Tue/Thu)",
        "branch": "Downtown Branch",
        "status": StudentStatusEnum.ACTIVE,
        "tuition_status": TuitionStatusEnum.PENDING,
        "balance": 160.0,
        "attendance_rate": 92,
        "enrolled_at": "2026-08-20"
    },
    {
        "id": "student-3",
        "student_id": "STU-2026-003",
        "name": "Seo-yeon Lee",
        "email": "seoyeon.lee@student.edu",
        "phone": "010-9123-4567",
        "course_id": "course-korean",
        "course_name": "Korean Language",
        "group_name": "TOPIK II Weekend Intensive",
        "branch": "Central Campus",
        "status": StudentStatusEnum.ACTIVE,
        "tuition_status": TuitionStatusEnum.PAID,
        "balance": 0.0,
        "attendance_rate": 100,
        "enrolled_at": "2026-07-10"
    },
    {
        "id": "student-4",
        "student_id": "STU-2026-004",
        "name": "Alex Johnson",
        "email": "alex.johnson@student.edu",
        "phone": "+1 (555) 019-6102",
        "course_id": "course-starter",
        "course_name": "Starter",
        "group_name": "Starter A1 Morning (Mon-Fri)",
        "branch": "Central Campus",
        "status": StudentStatusEnum.ON_LEAVE,
        "tuition_status": TuitionStatusEnum.PAID,
        "balance": 0.0,
        "attendance_rate": 88,
        "enrolled_at": "2026-06-01"
    },
    {
        "id": "student-5",
        "student_id": "STU-2026-005",
        "name": "Ha-eun Jung",
        "email": "haeun.jung@student.edu",
        "phone": "010-2233-4455",
        "guardian_name": "Sang-hoon Jung",
        "guardian_phone": "010-9988-7766",
        "course_id": "course-intermediate",
        "course_name": "Intermediate",
        "group_name": "Conversation Club (Tue/Thu)",
        "branch": "Downtown Branch",
        "status": StudentStatusEnum.ACTIVE,
        "tuition_status": TuitionStatusEnum.OVERDUE,
        "balance": 240.0,
        "attendance_rate": 85,
        "enrolled_at": "2026-08-01"
    },
    {
        "id": "student-6",
        "student_id": "STU-2026-006",
        "name": "Marcus Vance",
        "email": "marcus.vance@student.edu",
        "phone": "+1 (415) 555-0199",
        "course_id": "course-korean",
        "course_name": "Korean Language",
        "group_name": "Expat Practical Korean (Evening)",
        "branch": "Central Campus",
        "status": StudentStatusEnum.ACTIVE,
        "tuition_status": TuitionStatusEnum.PAID,
        "balance": 0.0,
        "attendance_rate": 95,
        "enrolled_at": "2026-08-25"
    },
    {
        "id": "student-7",
        "student_id": "STU-2026-007",
        "name": "Dong-hyun Choi",
        "email": "donghyun.choi@student.edu",
        "phone": "010-4455-6677",
        "course_id": "course-advanced",
        "course_name": "Advanced",
        "group_name": "C1 Academic Writing & Debate",
        "branch": "Central Campus",
        "status": StudentStatusEnum.GRADUATED,
        "tuition_status": TuitionStatusEnum.PAID,
        "balance": 0.0,
        "attendance_rate": 99,
        "enrolled_at": "2026-01-15"
    },
    {
        "id": "student-8",
        "student_id": "STU-2026-008",
        "name": "Chloe Dubois",
        "email": "chloe.dubois@student.edu",
        "phone": "+33 6 12 34 56 78",
        "course_id": "course-chinese",
        "course_name": "Chinese (Mandarin)",
        "group_name": "HSK 3 Fast-Track",
        "branch": "Downtown Branch",
        "status": StudentStatusEnum.ACTIVE,
        "tuition_status": TuitionStatusEnum.PAID,
        "balance": 0.0,
        "attendance_rate": 94,
        "enrolled_at": "2026-08-12"
    },
    {
        "id": "student-9",
        "student_id": "STU-2026-009",
        "name": "Ye-jun Kang",
        "email": "yejun.kang@student.edu",
        "phone": "010-3344-5566",
        "guardian_name": "Myung-hee Kang",
        "course_id": "course-ielts",
        "course_name": "IELTS Preparation",
        "group_name": "IELTS Weekend Prep",
        "branch": "Central Campus",
        "status": StudentStatusEnum.INACTIVE,
        "tuition_status": TuitionStatusEnum.OVERDUE,
        "balance": 320.0,
        "attendance_rate": 64,
        "enrolled_at": "2026-05-10"
    },
    {
        "id": "student-10",
        "student_id": "STU-2026-010",
        "name": "Soo-ah Shin",
        "email": "sooah.shin@student.edu",
        "phone": "010-7788-9900",
        "guardian_name": "Jin-woo Shin",
        "guardian_phone": "010-3322-1100",
        "course_id": "course-starter",
        "course_name": "Starter",
        "group_name": "Evening Foundations A",
        "branch": "Downtown Branch",
        "status": StudentStatusEnum.ACTIVE,
        "tuition_status": TuitionStatusEnum.PAID,
        "balance": 0.0,
        "attendance_rate": 96,
        "enrolled_at": "2026-09-01"
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

        # Seed students
        for s in DEMO_STUDENTS:
            existing_student = db.query(Student).filter(Student.id == s["id"]).first()
            if not existing_student:
                student = Student(
                    id=s["id"],
                    student_id=s["student_id"],
                    name=s["name"],
                    email=s["email"],
                    phone=s["phone"],
                    guardian_name=s.get("guardian_name"),
                    guardian_phone=s.get("guardian_phone"),
                    course_id=s["course_id"],
                    course_name=s["course_name"],
                    group_name=s["group_name"],
                    branch=s["branch"],
                    status=s["status"],
                    tuition_status=s["tuition_status"],
                    balance=s["balance"],
                    attendance_rate=s.get("attendance_rate", 100),
                    enrolled_at=s["enrolled_at"]
                )
                db.add(student)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database with platform roles, courses, leads, and students...")
    init_db()
    print("Database seeded successfully!")

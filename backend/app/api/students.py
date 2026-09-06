from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import secrets

from backend.app.database import get_db
from backend.app.models.student import Student, StudentStatusEnum, TuitionStatusEnum
from backend.app.models.course import Course

router = APIRouter(prefix="/students", tags=["Students"])

class StudentCreate(BaseModel):
    name: str
    email: str
    phone: str
    course_id: str
    group_name: str
    branch: Optional[str] = "Central Campus"
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    notes: Optional[str] = None

class StudentOut(BaseModel):
    id: str
    studentId: str
    name: str
    email: str
    phone: str
    guardianName: Optional[str] = None
    guardianPhone: Optional[str] = None
    courseId: str
    courseName: str
    groupName: str
    branch: str
    status: StudentStatusEnum
    tuitionStatus: TuitionStatusEnum
    balance: float
    attendanceRate: Optional[int] = 100
    enrolledAt: str
    notes: Optional[str] = None

@router.get("", response_model=List[StudentOut])
def get_students(
    search: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    branch: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all students with optional search and filters."""
    query = db.query(Student)

    if course_id and course_id != "all":
        query = query.filter(Student.course_id == course_id)
    if status and status != "all":
        query = query.filter(Student.status == status)
    if branch and branch != "all":
        query = query.filter(Student.branch == branch)

    students = query.order_by(Student.name.asc()).all()

    if search:
        s_term = search.lower().strip()
        students = [
            s for s in students
            if s_term in s.name.lower() or
               s_term in s.student_id.lower() or
               s_term in s.phone.replace("-", "") or
               s_term in s.email.lower()
        ]

    return [
        StudentOut(
            id=s.id,
            studentId=s.student_id,
            name=s.name,
            email=s.email,
            phone=s.phone,
            guardianName=s.guardian_name,
            guardianPhone=s.guardian_phone,
            courseId=s.course_id,
            courseName=s.course_name,
            groupName=s.group_name,
            branch=s.branch,
            status=s.status,
            tuitionStatus=s.tuition_status,
            balance=s.balance,
            attendanceRate=s.attendance_rate,
            enrolledAt=s.enrolled_at,
            notes=s.notes
        )
        for s in students
    ]

@router.post("", response_model=StudentOut)
def enroll_student(data: StudentCreate, db: Session = Depends(get_db)):
    """Enroll a new student."""
    course = db.query(Course).filter(Course.id == data.course_id).first()
    course_name = course.name if course else "General Program"

    count = db.query(Student).count() + 1
    student_id = f"STU-2026-{str(count).zfill(3)}"

    new_student = Student(
        id=f"stu-{secrets.token_hex(4)}",
        student_id=student_id,
        name=data.name.strip(),
        email=data.email.strip(),
        phone=data.phone.strip(),
        guardian_name=data.guardian_name,
        guardian_phone=data.guardian_phone,
        course_id=data.course_id,
        course_name=course_name,
        group_name=data.group_name,
        branch=data.branch or "Central Campus",
        status=StudentStatusEnum.ACTIVE,
        tuition_status=TuitionStatusEnum.PAID,
        balance=0.0,
        attendance_rate=100,
        enrolled_at="2026-09-01",
        notes=data.notes
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return StudentOut(
        id=new_student.id,
        studentId=new_student.student_id,
        name=new_student.name,
        email=new_student.email,
        phone=new_student.phone,
        guardianName=new_student.guardian_name,
        guardianPhone=new_student.guardian_phone,
        courseId=new_student.course_id,
        courseName=new_student.course_name,
        groupName=new_student.group_name,
        branch=new_student.branch,
        status=new_student.status,
        tuitionStatus=new_student.tuition_status,
        balance=new_student.balance,
        attendanceRate=new_student.attendance_rate,
        enrolledAt=new_student.enrolled_at,
        notes=new_student.notes
    )

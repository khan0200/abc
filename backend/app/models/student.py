from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, Enum as SQLEnum, Text, ForeignKey
from backend.app.database import Base

class StudentStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    ON_LEAVE = "ON_LEAVE"
    GRADUATED = "GRADUATED"
    INACTIVE = "INACTIVE"

class TuitionStatusEnum(str, Enum):
    PAID = "PAID"
    PENDING = "PENDING"
    OVERDUE = "OVERDUE"

class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    guardian_name = Column(String, nullable=True)
    guardian_phone = Column(String, nullable=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    course_name = Column(String, nullable=False)
    group_name = Column(String, nullable=False)
    branch = Column(String, nullable=False, default="Central Campus")
    status = Column(SQLEnum(StudentStatusEnum), default=StudentStatusEnum.ACTIVE, nullable=False, index=True)
    tuition_status = Column(SQLEnum(TuitionStatusEnum), default=TuitionStatusEnum.PAID, nullable=False)
    balance = Column(Float, default=0.0)
    attendance_rate = Column(Integer, default=100)
    enrolled_at = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.student_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "guardianName": self.guardian_name,
            "guardianPhone": self.guardian_phone,
            "courseId": self.course_id,
            "courseName": self.course_name,
            "groupName": self.group_name,
            "branch": self.branch,
            "status": self.status.value,
            "tuitionStatus": self.tuition_status.value,
            "balance": self.balance,
            "attendanceRate": self.attendance_rate,
            "enrolledAt": self.enrolled_at,
            "notes": self.notes
        }

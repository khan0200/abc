from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Text, ForeignKey
from backend.app.database import Base

class LeadStatusEnum(str, Enum):
    COLD = "COLD"
    WAITING = "WAITING"
    CLOSED = "CLOSED"

class ClosedReasonEnum(str, Enum):
    NO_ANSWER = "NO_ANSWER"
    WRONG_NUMBER = "WRONG_NUMBER"
    IRRELEVANT = "IRRELEVANT"
    OTHER = "OTHER"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    course_name = Column(String, nullable=False)
    status = Column(SQLEnum(LeadStatusEnum), default=LeadStatusEnum.COLD, nullable=False, index=True)
    closed_reason = Column(SQLEnum(ClosedReasonEnum), nullable=True)
    source = Column(String, nullable=True)
    preferred_start_date = Column(String, nullable=True)
    preferred_time = Column(String, nullable=True)
    assigned_manager = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "courseId": self.course_id,
            "courseName": self.course_name,
            "status": self.status.value,
            "closedReason": self.closed_reason.value if self.closed_reason else None,
            "source": self.source,
            "preferredStartDate": self.preferred_start_date,
            "preferredTime": self.preferred_time,
            "assignedManager": self.assigned_manager,
            "notes": self.notes,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }

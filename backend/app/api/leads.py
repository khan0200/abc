from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import secrets

from backend.app.database import get_db
from backend.app.models.lead import Lead, LeadStatusEnum, ClosedReasonEnum
from backend.app.models.course import Course

router = APIRouter(prefix="/leads", tags=["Leads"])

class LeadCreate(BaseModel):
    name: str
    phone: str
    course_id: str
    notes: Optional[str] = None
    source: Optional[str] = "Direct Entry"
    preferred_start_date: Optional[str] = None
    preferred_time: Optional[str] = None
    assigned_manager: Optional[str] = None

class LeadStatusUpdate(BaseModel):
    status: LeadStatusEnum
    closed_reason: Optional[ClosedReasonEnum] = None

class LeadOut(BaseModel):
    id: str
    name: str
    phone: str
    courseId: str
    courseName: str
    status: LeadStatusEnum
    closedReason: Optional[ClosedReasonEnum] = None
    notes: Optional[str] = None
    source: Optional[str] = None
    preferredStartDate: Optional[str] = None
    preferredTime: Optional[str] = None
    assignedManager: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

@router.get("", response_model=List[LeadOut])
def get_leads(db: Session = Depends(get_db)):
    """Retrieve all leads for Kanban board."""
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return [
        LeadOut(
            id=l.id,
            name=l.name,
            phone=l.phone,
            courseId=l.course_id,
            courseName=l.course_name,
            status=l.status,
            closedReason=l.closed_reason,
            notes=l.notes,
            source=l.source,
            preferredStartDate=l.preferred_start_date,
            preferredTime=l.preferred_time,
            assignedManager=l.assigned_manager,
            createdAt=l.created_at.isoformat() if l.created_at else None,
            updatedAt=l.updated_at.isoformat() if l.updated_at else None
        )
        for l in leads
    ]

@router.post("", response_model=LeadOut)
def create_lead(data: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead and automatically place into Cold column."""
    course = db.query(Course).filter(Course.id == data.course_id).first()
    course_name = course.name if course else "General Course"

    new_lead = Lead(
        id=f"lead-{secrets.token_hex(4)}",
        name=data.name.strip(),
        phone=data.phone.strip(),
        course_id=data.course_id,
        course_name=course_name,
        status=LeadStatusEnum.COLD,
        notes=data.notes.strip() if data.notes else None,
        source=data.source,
        preferred_start_date=data.preferred_start_date,
        preferred_time=data.preferred_time,
        assigned_manager=data.assigned_manager or "Unassigned",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return LeadOut(
        id=new_lead.id,
        name=new_lead.name,
        phone=new_lead.phone,
        courseId=new_lead.course_id,
        courseName=new_lead.course_name,
        status=new_lead.status,
        closedReason=new_lead.closed_reason,
        notes=new_lead.notes,
        source=new_lead.source,
        preferredStartDate=new_lead.preferred_start_date,
        preferredTime=new_lead.preferred_time,
        assignedManager=new_lead.assigned_manager,
        createdAt=new_lead.created_at.isoformat() if new_lead.created_at else None,
        updatedAt=new_lead.updated_at.isoformat() if new_lead.updated_at else None
    )

@router.patch("/{lead_id}/status", response_model=LeadOut)
def update_lead_status(lead_id: str, data: LeadStatusUpdate, db: Session = Depends(get_db)):
    """Update lead status when dragged between Kanban columns."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.status = data.status
    if data.status == LeadStatusEnum.CLOSED:
        lead.closed_reason = data.closed_reason or ClosedReasonEnum.NO_ANSWER
    else:
        lead.closed_reason = None

    lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(lead)

    return LeadOut(
        id=lead.id,
        name=lead.name,
        phone=lead.phone,
        courseId=lead.course_id,
        courseName=lead.course_name,
        status=lead.status,
        closedReason=lead.closed_reason,
        notes=lead.notes,
        source=lead.source,
        preferredStartDate=lead.preferred_start_date,
        preferredTime=lead.preferred_time,
        assignedManager=lead.assigned_manager,
        createdAt=lead.created_at.isoformat() if lead.created_at else None,
        updatedAt=lead.updated_at.isoformat() if lead.updated_at else None
    )

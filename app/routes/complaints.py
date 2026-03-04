from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import schemas
from ..utils.dependencies import get_current_user, check_role
from ..services import email_service

router = APIRouter(prefix="/complaints", tags=["Complaints"])

@router.post("/", response_model=schemas.ComplaintOut)
def create_complaint(
    complaint: schemas.ComplaintCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_complaint = models.Complaint(
        **complaint.dict(), 
        user_id=current_user.id
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    return new_complaint

@router.get("/", response_model=List[schemas.ComplaintOut])
def read_complaints(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Students see only their complaints, Wardens/Admins see all
    query = db.query(models.Complaint)
    if current_user.role == "student":
        query = query.filter(models.Complaint.user_id == current_user.id)
    
    complaints = query.offset(skip).limit(limit).all()
    return complaints

@router.patch("/{complaint_id}", response_model=schemas.ComplaintOut)
def update_complaint_status(
    complaint_id: int, 
    update: schemas.ComplaintUpdate, 
    db: Session = Depends(get_db),
    warden_user: models.User = Depends(check_role(["warden", "admin"]))
):
    complaint = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    complaint.status = update.status
    db.commit()
    db.refresh(complaint)
    
    # Notify student
    student = db.query(models.User).filter(models.User.id == complaint.user_id).first()
    if student:
        email_service.notify_complaint_update(student.email, complaint.title, update.status)
        
    return complaint

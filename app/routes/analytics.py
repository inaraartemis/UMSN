from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import models
from ..utils.dependencies import check_role

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/occupancy")
def get_occupancy_stats(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin"]))
):
    total_rooms = db.query(models.Room).count()
    total_capacity = db.query(func.sum(models.Room.capacity)).scalar() or 0
    occupied_beds = db.query(func.sum(models.Room.occupied_count)).scalar() or 0
    
    return {
        "total_rooms": total_rooms,
        "total_capacity": total_capacity,
        "occupied_beds": occupied_beds,
        "occupancy_rate": (occupied_beds / total_capacity * 100) if total_capacity > 0 else 0
    }

@router.get("/revenue")
def get_revenue_stats(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin"]))
):
    total_revenue = db.query(func.sum(models.Payment.amount)).filter(models.Payment.status == "paid").scalar() or 0
    pending_revenue = db.query(func.sum(models.Payment.amount)).filter(models.Payment.status == "pending").scalar() or 0
    
    return {
        "total_revenue_collected": total_revenue,
        "pending_revenue": pending_revenue
    }

@router.get("/complaints")
def get_complaint_stats(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin", "warden"]))
):
    stats = db.query(models.Complaint.status, func.count(models.Complaint.id)).group_by(models.Complaint.status).all()
    return {status: count for status, count in stats}

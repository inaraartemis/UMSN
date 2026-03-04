from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import schemas
from ..utils.dependencies import get_current_user, check_role

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=schemas.PaymentOut)
def create_payment(
    payment: schemas.PaymentCreate, 
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin"]))
):
    new_payment = models.Payment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/", response_model=List[schemas.PaymentOut])
def read_payments(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Payment)
    if current_user.role == "student":
        query = query.filter(models.Payment.user_id == current_user.id)
    
    payments = query.offset(skip).limit(limit).all()
    return payments

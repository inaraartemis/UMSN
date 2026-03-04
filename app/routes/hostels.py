from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import schemas
from ..utils.dependencies import check_role

router = APIRouter(prefix="/hostels", tags=["Hostels"])

@router.post("/", response_model=schemas.HostelOut)
def create_hostel(
    hostel: schemas.HostelCreate, 
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin"]))
):
    db_hostel = db.query(models.Hostel).filter(models.Hostel.name == hostel.name).first()
    if db_hostel:
        raise HTTPException(status_code=400, detail="Hostel name already exists")
    new_hostel = models.Hostel(**hostel.dict())
    db.add(new_hostel)
    db.commit()
    db.refresh(new_hostel)
    return new_hostel

@router.get("/", response_model=List[schemas.HostelOut])
def read_hostels(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    hostels = db.query(models.Hostel).offset(skip).limit(limit).all()
    return hostels

@router.get("/{hostel_id}", response_model=schemas.HostelOut)
def read_hostel(hostel_id: int, db: Session = Depends(get_db)):
    hostel = db.query(models.Hostel).filter(models.Hostel.id == hostel_id).first()
    if not hostel:
        raise HTTPException(status_code=404, detail="Hostel not found")
    return hostel

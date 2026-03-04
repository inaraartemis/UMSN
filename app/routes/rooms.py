from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import models
from ..schemas import schemas
from ..utils.dependencies import get_current_user, check_role
from ..services import email_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/allocations", response_model=List[schemas.AllocationOut], tags=["Allocations"])
def list_allocations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin", "warden"]))
):
    return db.query(models.Allocation).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.RoomOut)
def create_room(
    room: schemas.RoomCreate, 
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin"]))
):
    db_room = db.query(models.Room).filter(models.Room.room_number == room.room_number).first()
    if db_room:
        raise HTTPException(status_code=400, detail="Room number already exists")
    new_room = models.Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/", response_model=List[schemas.RoomOut])
def read_rooms(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    rooms = db.query(models.Room).offset(skip).limit(limit).all()
    return rooms

@router.post("/{room_id}/allocate", response_model=schemas.AllocationOut)
def allocate_room(
    room_id: int, 
    user_id: int, 
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin", "warden"]))
):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.occupied_count >= room.capacity:
        raise HTTPException(status_code=400, detail="Room is at full capacity")
    
    # Check if student already has an active allocation
    active_alloc = db.query(models.Allocation).filter(
        models.Allocation.user_id == user_id, 
        models.Allocation.is_active == True
    ).first()
    if active_alloc:
        raise HTTPException(status_code=400, detail="Student already has an active room allocation")

    new_allocation = models.Allocation(user_id=user_id, room_id=room_id)
    room.occupied_count += 1
    
    db.add(new_allocation)
    db.commit()
    db.refresh(new_allocation)
    
    # Notify student
    student = db.query(models.User).filter(models.User.id == user_id).first()
    if student:
        email_service.notify_room_allocation(student.email, room.room_number)
        
    return new_allocation

@router.post("/{room_id}/vacate", response_model=schemas.AllocationOut)
def vacate_room(
    room_id: int, 
    user_id: int, 
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(check_role(["admin", "warden"]))
):
    allocation = db.query(models.Allocation).filter(
        models.Allocation.room_id == room_id,
        models.Allocation.user_id == user_id,
        models.Allocation.is_active == True
    ).first()
    
    if not allocation:
        raise HTTPException(status_code=404, detail="Active allocation not found for this student and room")
    
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    allocation.is_active = False
    allocation.end_date = datetime.utcnow()
    room.occupied_count -= 1
    
    db.commit()
    db.refresh(allocation)
    return allocation

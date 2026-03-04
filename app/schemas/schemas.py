from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from ..models.models import UserRole, ComplaintStatus, ComplaintPriority

# Base Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.STUDENT

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

class UserOut(UserBase):
    id: int
    is_verified: bool
    created_at: datetime
    class Config:
        from_attributes = True

# Hostel Schemas
class HostelBase(BaseModel):
    name: str
    address: str
    total_rooms: int = 0

class HostelCreate(HostelBase):
    pass

class HostelOut(HostelBase):
    id: int
    class Config:
        from_attributes = True

# Room Schemas
class RoomBase(BaseModel):
    room_number: str
    hostel_id: int
    capacity: int

class RoomCreate(RoomBase):
    pass

class RoomOut(RoomBase):
    id: int
    occupied_count: int
    class Config:
        from_attributes = True

# Allocation Schemas
class AllocationBase(BaseModel):
    user_id: int
    room_id: int

class AllocationCreate(AllocationBase):
    pass

class AllocationOut(AllocationBase):
    id: int
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool
    class Config:
        from_attributes = True

# Complaint Schemas
class ComplaintBase(BaseModel):
    title: str
    description: str
    priority: ComplaintPriority = ComplaintPriority.MEDIUM

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    status: ComplaintStatus

class ComplaintOut(ComplaintBase):
    id: int
    user_id: int
    status: ComplaintStatus
    created_at: datetime
    class Config:
        from_attributes = True

# Payment Schemas
class PaymentBase(BaseModel):
    user_id: int
    amount: float
    status: str = "pending"

class PaymentCreate(PaymentBase):
    pass

class PaymentOut(PaymentBase):
    id: int
    payment_date: datetime
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

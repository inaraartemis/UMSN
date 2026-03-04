from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    WARDEN = "warden"
    STUDENT = "student"

class ComplaintStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class ComplaintPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default=UserRole.STUDENT)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    allocations = relationship("Allocation", back_populates="user")
    complaints = relationship("Complaint", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Hostel(Base):
    __tablename__ = "hostels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)
    total_rooms = Column(Integer, default=0)

    rooms = relationship("Room", back_populates="hostel")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"))
    capacity = Column(Integer)
    occupied_count = Column(Integer, default=0)

    hostel = relationship("Hostel", back_populates="rooms")
    allocations = relationship("Allocation", back_populates="room")

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="allocations")
    room = relationship("Room", back_populates="allocations")

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    priority = Column(String, default=ComplaintPriority.MEDIUM)
    status = Column(String, default=ComplaintStatus.OPEN)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="complaints")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    status = Column(String, default="pending") # pending, paid
    payment_date = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="payments")

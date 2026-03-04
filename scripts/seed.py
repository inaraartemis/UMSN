import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import models
from app.core import security

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(models.User).filter(models.User.role == "admin").first():
            print("Database already seeded.")
            return

        print("Seeding database with Indian demo data...")

        # ── Users ──────────────────────────────────────────────
        admin = models.User(name="Admin", email="admin@hostel.com",
            password_hash=security.get_password_hash("admin123"), role="admin", is_verified=True)

        wardens = [
            models.User(name="Rekha Sharma",    email="warden@hostel.com",
                password_hash=security.get_password_hash("warden123"), role="warden", is_verified=True),
            models.User(name="Suresh Iyer",     email="warden2@hostel.com",
                password_hash=security.get_password_hash("warden123"), role="warden", is_verified=True),
        ]

        students = [
            models.User(name="Arpita Mahapatra",  email="student@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Priya Nair",         email="priya.nair@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Rohan Banerjee",     email="rohan.banerjee@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Ananya Krishnan",    email="ananya.k@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Vikram Patel",       email="vikram.patel@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Sneha Pillai",       email="sneha.pillai@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Arjun Mehta",        email="arjun.mehta@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Kavya Reddy",        email="kavya.reddy@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Siddharth Rao",      email="sid.rao@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
            models.User(name="Meera Joshi",        email="meera.joshi@hostel.com",
                password_hash=security.get_password_hash("student123"), role="student", is_verified=True),
        ]

        db.add(admin)
        db.add_all(wardens)
        db.add_all(students)
        db.commit()
        for s in students: db.refresh(s)

        # ── Hostels ────────────────────────────────────────────
        h1 = models.Hostel(name="Saraswati Bhavan",   address="Block A, North Campus", total_rooms=40)
        h2 = models.Hostel(name="Vivekananda Niwas",  address="Block B, South Campus", total_rooms=35)
        h3 = models.Hostel(name="Tagore Residence",   address="Block C, East Campus",  total_rooms=30)
        db.add_all([h1, h2, h3])
        db.commit()
        for h in [h1, h2, h3]: db.refresh(h)

        # ── Rooms ──────────────────────────────────────────────
        rooms_h1 = [
            models.Room(room_number="A101", capacity=2, hostel_id=h1.id),
            models.Room(room_number="A102", capacity=2, hostel_id=h1.id),
            models.Room(room_number="A103", capacity=3, hostel_id=h1.id),
            models.Room(room_number="A104", capacity=4, hostel_id=h1.id),
            models.Room(room_number="A201", capacity=2, hostel_id=h1.id),
        ]
        rooms_h2 = [
            models.Room(room_number="B101", capacity=2, hostel_id=h2.id),
            models.Room(room_number="B102", capacity=2, hostel_id=h2.id),
            models.Room(room_number="B103", capacity=3, hostel_id=h2.id),
            models.Room(room_number="B201", capacity=2, hostel_id=h2.id),
        ]
        rooms_h3 = [
            models.Room(room_number="C101", capacity=2, hostel_id=h3.id),
            models.Room(room_number="C102", capacity=3, hostel_id=h3.id),
            models.Room(room_number="C201", capacity=2, hostel_id=h3.id),
        ]
        all_rooms = rooms_h1 + rooms_h2 + rooms_h3
        db.add_all(all_rooms)
        db.commit()
        for r in all_rooms: db.refresh(r)

        # ── Allocations ────────────────────────────────────────
        alloc_map = [
            (students[0], rooms_h1[0]),   # Arpita → A101
            (students[1], rooms_h1[0]),   # Priya  → A101 (same room, 2-seater)
            (students[2], rooms_h1[1]),   # Rohan  → A102
            (students[3], rooms_h2[0]),   # Ananya → B101
            (students[4], rooms_h2[0]),   # Vikram → B101
            (students[5], rooms_h2[2]),   # Sneha  → B103
            (students[6], rooms_h3[0]),   # Arjun  → C101
            (students[7], rooms_h3[0]),   # Kavya  → C101
        ]
        for student, room in alloc_map:
            db.add(models.Allocation(user_id=student.id, room_id=room.id))
            room.occupied_count = (room.occupied_count or 0) + 1
        db.commit()

        # ── Complaints ─────────────────────────────────────────
        complaints_data = [
            (students[0].id, "Fan not working",          "Ceiling fan in A101 makes noise and spins slowly.",           "medium", "open"),
            (students[1].id, "Water leakage",            "Bathroom tap leaking since 3 days, floor is always wet.",     "high",   "in_progress"),
            (students[2].id, "Broken desk chair",        "Chair leg is broken, cannot sit comfortably to study.",       "low",    "resolved"),
            (students[3].id, "No hot water",             "Geyser in B101 not working since Monday.",                    "high",   "open"),
            (students[4].id, "WiFi not working",         "Room B101 has very weak WiFi signal, barely usable.",         "medium", "open"),
            (students[5].id, "Window latch broken",      "Window in B103 won't close properly, insects entering.",      "medium", "in_progress"),
            (students[6].id, "Light flickering",         "Tube light in C101 flickers constantly, causing headaches.",  "low",    "resolved"),
            (students[7].id, "Mattress needs replacement", "Mattress is torn and uncomfortable, need a new one.",       "medium", "open"),
            (students[8].id, "Noisy pipes",              "Water pipes in washroom make loud sounds at night.",          "low",    "open"),
            (students[0].id, "Almirah lock broken",      "Cabinet lock is jammed, cannot access belongings.",           "high",   "in_progress"),
        ]
        for uid, title, desc, priority, status in complaints_data:
            db.add(models.Complaint(user_id=uid, title=title, description=desc, priority=priority, status=status))
        db.commit()

        # ── Payments ───────────────────────────────────────────
        payments_data = [
            (students[0].id, 8500.0,  "paid"),
            (students[1].id, 8500.0,  "paid"),
            (students[2].id, 7800.0,  "paid"),
            (students[3].id, 9200.0,  "paid"),
            (students[4].id, 9200.0,  "pending"),
            (students[5].id, 8000.0,  "paid"),
            (students[6].id, 7500.0,  "pending"),
            (students[7].id, 7500.0,  "paid"),
            (students[8].id, 8800.0,  "paid"),
            (students[9].id, 8800.0,  "pending"),
        ]
        for uid, amount, status in payments_data:
            db.add(models.Payment(user_id=uid, amount=amount, status=status))
        db.commit()

        print("DONE: Seeded 12 users (1 admin, 2 wardens, 10 students)")
        print("DONE: Seeded 3 hostels — Saraswati Bhavan, Vivekananda Niwas, Tagore Residence")
        print("DONE: Seeded 13 rooms across all hostels")
        print("DONE: Seeded 8 allocations")
        print("DONE: Seeded 10 complaints (mix of open / in-progress / resolved)")
        print("DONE: Seeded 10 payments (mix of paid / pending)")
        print("\nSeeding complete!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_db()

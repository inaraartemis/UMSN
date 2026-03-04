# 🏠 Abode - Smart Residential Management System

**Abode** is a premium, high-performance residential management platform designed for modern universities. It combines a robust **FastAPI** backend with a sophisticated, highly-customizable standalone UI to provide a seamless experience for students, wardens, and administrators.

![Theme Preview](https://img.shields.io/badge/Theme-Twilight_Lavender-blueviolet?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI_|_SQLite_|_Vanilla_JS-teal?style=for-the-badge)

---

## ✨ Key Features

### 👤 User Roles & Auth
- **Admin:** Full system oversight, user management, and analytics.
- **Warden:** Hostel-specific control, room allocation, and complaint resolution.
- **Student:** Room details, maintenance requests, and payment history.
- **JWT-based Security:** Secure, token-based authentication flow.

### 🏢 Residential Management
- **Hostel Tracking:** Manage multiple buildings (e.g., *Saraswati Bhavan*, *Vivekananda Niwas*) with detailed attributes.
- **Intelligent Allocation:** Automated room assignment with real-time vacancy tracking.
- **Maintenance (Complaints):** Localized maintenance tracking with status updates (Open → In-Progress → Resolved).

### 💰 Finance & Payments
- **Fee Management:** Track hostel fees and payment statuses.
- **History:** Comprehensive localized payment history for students.

---

## 🎨 Aesthetic & Themes
Abode is built to be "soothing to look at." The current active theme is **Twilight Lavender**, a dreamy combination of lilac accents and deep indigo tones.

| Feature | Description |
| :--- | :--- |
| **Theme** | Twilight Lavender (Lilac, Twilight Blue, Deep Indigo) |
| **Typography** | Inter (Premium-scaled weights) |
| **Background** | Deep Twilight / Auburn gradients |
| **Components** | Glassmorphic cards, curved sidebars, and micro-animations |

---

## 🛠️ Tech Stack

### Backend
- **Core:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database:** SQLite (default) / PostgreSQL support
- **Auth:** JWT (Jose) & Passlib (Bcrypt)

### Frontend
- **Structure:** Standalone Vanilla HTML5
- **Logic:** Native JavaScript (ES6+)
- **Styling:** Premium Custom CSS (Grid & Flexbox)
- **Icons:** Lucide-SVG

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11 or higher.

### 2. Backend Setup
```bash
# Clone the repository
git clone https://github.com/inaraartemis/UMSN.git
cd UMSN

# Install dependencies
pip install -r requirements_hostel.txt

# Seed the database with Indian demo data
python scripts/seed.py

# Run the server
uvicorn app.main:app --reload
```

### 3. Frontend Access
Simply open the local files in your browser:
- **Login:** `hostel_ui/index.html`
- **Dashboard:** `hostel_ui/dashboard.html` (Accessible after login)

### 🔑 Demo Credentials
- **Admin:** `admin@hostel.com` / `admin123`
- **Student:** `student@hostel.com` / `student123`

---

## 🇮🇳 Localized Demo Data
The system comes pre-populated with realistic Indian data:
- **Names:** Arpita Mahapatra, Rekha Sharma, Suresh Iyer, Rohan Banerjee, etc.
- **Locations:** Saraswati Bhavan, Tagore Residence, etc.
- **Scenarios:** Common maintenance issues (Geyser not working, Fan noise, etc.)

---

## 📖 API Documentation
Once the server is running, access the interactive docs at:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

*Created for the University Management System project.*
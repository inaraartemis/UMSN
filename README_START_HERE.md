# 🏨 Smart Hostel Management System - Quick Start Guide

Follow these steps exactly to run your backend and see the premium UI.

## Part 1: Run the Backend API (FastAPI)

1. **Open a Terminal** (PowerShell or CMD) in the project folder: `d:\work\Class Projects\UMS`
2. **Install Dependencies**:
   ```powershell
   python -m pip install -r requirements_hostel.txt
   ```
3. **Initialize & Seed Database**:
   This creates the rooms and demo users.
   ```powershell
   python scripts/seed.py
   ```
4. **Start the Server**:
   ```powershell
   python -m uvicorn app.main:app --reload
   ```
   *Keep this terminal open! Your backend is now running at `http://localhost:8000`.*

---

## Part 2: See the Premium UI (Nice Design)

Since you don't have NPM, follow these steps to see the design:

1. **Open File Explorer** and go to `d:\work\Class Projects\UMS`.
2. Find the file: **`RE_DESIGN_PREVIEW.html`**.
3. **Double-click it** to open it in your browser.
4. **Enjoy!** You can see the full dashboard with charts and stats.

---

## 🔑 Demo Credentials
If you want to test the API directly via `/docs`:
- **Admin**: `admin@hostel.com` / `admin123`
- **Student**: `student@hostel.com` / `student123`

---

## 📁 Project Structure
- `app/`: All backend Python code.
- `scripts/seed.py`: Script to reset/setup your data.
- `RE_DESIGN_PREVIEW.html`: Your "Nice" UI preview file.

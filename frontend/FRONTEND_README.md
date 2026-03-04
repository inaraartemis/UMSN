# 🎨 Smart Hostel Frontend - UI/UX Guide

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Node.js 18+** installed.

### 2. Installation
Navigate to the `frontend` directory and install dependencies:
```bash
cd frontend
npm install
```

### 3. Running in Development
Start the Vite development server:
```bash
npm run dev
```
The UI will be available at `http://localhost:3000`.

---

## ✨ Design System
- **Framework**: React 18
- **Styling**: Tailwind CSS (Dark Mode by default)
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Charts**: Recharts

## 📁 Key Components
- `src/App.jsx`: Main routing and Auth protected routes.
- `src/pages/Login.jsx`: Animated glassmorphism login with API integration.
- `src/pages/Dashboard.jsx`: Analytics overview with interactive charts.
- `src/components/Sidebar.jsx`: Dynamic navigation based on user roles (`admin`, `warden`, `student`).

---

## 🔧 Backend Integration
The frontend is configured with a **Vite Proxy** in `vite.config.js`. 
All requests to `/api/*` are automatically forwarded to your FastAPI backend at `http://localhost:8000`.

### Troubleshooting
If you see `ImportError` or `ModuleNotFoundError` during `npm install`, ensure your shell allows script execution or use a standard CMD/Git Bash.

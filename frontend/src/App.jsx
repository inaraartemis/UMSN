import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Sidebar from './components/Sidebar';

function App() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const savedUser = localStorage.getItem('user');
        if (savedUser) {
            setUser(JSON.parse(savedUser));
        }
        setLoading(false);
    }, []);

    if (loading) return null;

    return (
        <Router>
            <div className="flex min-h-screen bg-slate-950 text-slate-100">
                {user && <Sidebar user={user} setUser={setUser} />}
                <main className={`flex-1 ${user ? 'p-8' : ''}`}>
                    <Routes>
                        <Route
                            path="/login"
                            element={!user ? <Login setUser={setUser} /> : <Navigate to="/" />}
                        />
                        <Route
                            path="/"
                            element={user ? <Dashboard user={user} /> : <Navigate to="/login" />}
                        />
                        {/* Add more routes as we build pages */}
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App;

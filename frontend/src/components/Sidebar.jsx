import { NavLink, useNavigate } from 'react-router-dom';
import { Home, Bed, Link2, MessageSquare, CreditCard, PieChart, LogOut, ShieldCheck } from 'lucide-react';

const Sidebar = ({ user, setUser }) => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('user');
        setUser(null);
        navigate('/login');
    };

    const navItems = [
        { name: 'Dashboard', icon: <Home size={20} />, path: '/', roles: ['admin', 'warden', 'student'] },
        { name: 'Rooms', icon: <Bed size={20} />, path: '/rooms', roles: ['admin', 'warden'] },
        { name: 'Complaints', icon: <MessageSquare size={20} />, path: '/complaints', roles: ['admin', 'warden', 'student'] },
        { name: 'Payments', icon: <CreditCard size={20} />, path: '/payments', roles: ['admin', 'student'] },
        { name: 'Analytics', icon: <PieChart size={20} />, path: '/analytics', roles: ['admin'] },
    ];

    return (
        <aside className="w-64 glass-card m-4 flex flex-col border-r border-slate-800">
            <div className="p-6 flex items-center gap-3">
                <div className="p-2 bg-primary-600 rounded-lg shadow-lg shadow-primary-500/20">
                    <ShieldCheck className="text-white" />
                </div>
                <div>
                    <h1 className="font-bold text-lg tracking-tight">SmartHostel</h1>
                    <p className="text-xs text-slate-400 capitalize">{user.role}</p>
                </div>
            </div>

            <nav className="flex-1 px-4 py-2 space-y-1">
                {navItems.filter(item => item.roles.includes(user.role)).map((item) => (
                    <NavLink
                        key={item.name}
                        to={item.path}
                        className={({ isActive }) => `
              flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300
              ${isActive
                                ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20 shadow-lg shadow-primary-500/5'
                                : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'}
            `}
                    >
                        {item.icon}
                        <span className="font-medium">{item.name}</span>
                    </NavLink>
                ))}
            </nav>

            <div className="p-4 border-t border-slate-800">
                <div className="p-4 bg-slate-900/50 rounded-xl mb-4">
                    <p className="text-xs text-slate-500 mb-1">Signed in as</p>
                    <p className="font-medium truncate">{user.name}</p>
                </div>
                <button
                    onClick={handleLogout}
                    className="w-full flex items-center justify-center gap-2 px-4 py-3 text-red-400 hover:bg-red-400/5 rounded-xl transition-all duration-300 border border-transparent hover:border-red-400/20"
                >
                    <LogOut size={18} />
                    <span className="font-medium">Sign Out</span>
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;

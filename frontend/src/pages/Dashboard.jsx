import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, Bed, CreditCard, MessageSquare, TrendingUp, AlertCircle } from 'lucide-react';
import axios from 'axios';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = ({ user }) => {
    const [stats, setStats] = useState(null);
    const [complaints, setComplaints] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const config = { headers: { Authorization: `Bearer ${user.token}` } };

                if (user.role === 'admin' || user.role === 'warden') {
                    const [occRes, revRes, compRes] = await Promise.all([
                        axios.get('/api/analytics/occupancy', config),
                        axios.get('/api/analytics/revenue', config),
                        axios.get('/api/complaints', config)
                    ]);
                    setStats({ ...occRes.data, ...revRes.data });
                    setComplaints(compRes.data.slice(0, 5));
                } else {
                    const [payRes, compRes] = await Promise.all([
                        axios.get('/api/payments', config),
                        axios.get('/api/complaints', config)
                    ]);
                    setStats({ payments: payRes.data, complaintsCount: compRes.data.length });
                    setComplaints(compRes.data.slice(0, 5));
                }
            } catch (err) {
                console.error('Failed to fetch dashboard data', err);
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, [user]);

    const chartData = [
        { name: 'Mon', revenue: 4000 },
        { name: 'Tue', revenue: 3000 },
        { name: 'Wed', revenue: 5000 },
        { name: 'Thu', revenue: 2780 },
        { name: 'Fri', revenue: 1890 },
        { name: 'Sat', revenue: 2390 },
        { name: 'Sun', revenue: 3490 },
    ];

    if (loading) return null;

    return (
        <div className="space-y-8 animate-fade-in">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-white tracking-tight">System Overview</h1>
                    <p className="text-slate-400 mt-1">Welcome back, {user.name.split(' ')[0]}! Here's what's happening today.</p>
                </div>
                <div className="flex gap-3">
                    <div className="px-4 py-2 glass-card border-slate-800 flex items-center gap-2 text-sm text-slate-300">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                        System Live
                    </div>
                </div>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Occupancy"
                    value={`${stats?.occupancy_rate?.toFixed(1) || 0}%`}
                    subtitle={`${stats?.occupied_beds || 0} / ${stats?.total_capacity || 0} beds`}
                    icon={<Bed className="text-blue-400" />}
                    color="blue"
                />
                <StatCard
                    title="Total Revenue"
                    value={`$${stats?.total_revenue_collected || 0}`}
                    subtitle={`Pending: $${stats?.pending_revenue || 0}`}
                    icon={<CreditCard className="text-emerald-400" />}
                    color="emerald"
                />
                <StatCard
                    title="Complaints"
                    value={complaints.length}
                    subtitle="Total active tickets"
                    icon={<MessageSquare className="text-amber-400" />}
                    color="amber"
                />
                <StatCard
                    title="Active Students"
                    value={stats?.occupied_beds || 0}
                    subtitle="Allocated currently"
                    icon={<Users className="text-purple-400" />}
                    color="purple"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Chart Section */}
                <div className="lg:col-span-2 glass-card p-6 border-slate-800">
                    <div className="flex items-center justify-between mb-8">
                        <h3 className="font-semibold text-lg flex items-center gap-2">
                            <TrendingUp size={20} className="text-primary-500" />
                            Revenue Trends
                        </h3>
                        <select className="bg-slate-900 border border-slate-800 text-sm rounded-lg px-3 py-1 outline-none text-slate-400">
                            <option>Last 7 Days</option>
                            <option>Last 30 Days</option>
                        </select>
                    </div>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={chartData}>
                                <defs>
                                    <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                <XAxis dataKey="name" stroke="#64748b" axisLine={false} tickLine={false} tick={{ fontSize: 12 }} dy={10} />
                                <YAxis stroke="#64748b" axisLine={false} tickLine={false} tick={{ fontSize: 12 }} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px' }}
                                    itemStyle={{ color: '#0ea5e9' }}
                                />
                                <Area type="monotone" dataKey="revenue" stroke="#0ea5e9" strokeWidth={3} fillOpacity={1} fill="url(#colorRev)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Recent Activity */}
                <div className="glass-card p-6 border-slate-800">
                    <h3 className="font-semibold text-lg flex items-center gap-2 mb-6">
                        <AlertCircle size={20} className="text-primary-500" />
                        Recent Complaints
                    </h3>
                    <div className="space-y-4">
                        {complaints.map((c) => (
                            <div key={c.id} className="p-4 bg-slate-900/40 rounded-xl border border-slate-800/50 hover:border-slate-700 transition-colors group">
                                <div className="flex justify-between items-start mb-2">
                                    <span className={`text-[10px] px-2 py-0.5 rounded-full uppercase font-bold ${c.priority === 'high' ? 'bg-red-500/10 text-red-500' :
                                            c.priority === 'medium' ? 'bg-amber-500/10 text-amber-500' :
                                                'bg-blue-500/10 text-blue-500'
                                        }`}>
                                        {c.priority}
                                    </span>
                                    <span className="text-[10px] text-slate-500 uppercase">{c.status}</span>
                                </div>
                                <p className="text-sm font-medium text-slate-200 group-hover:text-primary-400 transition-colors">{c.title}</p>
                                <p className="text-xs text-slate-500 mt-1 line-clamp-1">{c.description}</p>
                            </div>
                        ))}
                        {complaints.length === 0 && (
                            <div className="text-center py-8 text-slate-500 italic text-sm">No recent tickets</div>
                        )}
                    </div>
                    <button className="w-full mt-6 py-3 text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-xl transition-all border border-transparent hover:border-slate-700">
                        View All Activity
                    </button>
                </div>
            </div>
        </div>
    );
};

const StatCard = ({ title, value, subtitle, icon, color }) => (
    <motion.div
        whileHover={{ y: -5 }}
        className="glass-card p-6 border-slate-800 relative group overflow-hidden"
    >
        <div className={`absolute -right-4 -bottom-4 w-24 h-24 rounded-full bg-${color}-500/5 blur-2xl group-hover:scale-150 transition-transform duration-700`} />
        <div className="flex items-center justify-between mb-4">
            <div className={`p-3 bg-${color}-500/10 rounded-xl`}>
                {icon}
            </div>
            <div className="text-xs text-slate-500 font-bold bg-slate-800/50 px-2 py-1 rounded-lg">+12%</div>
        </div>
        <h4 className="text-slate-400 text-sm font-medium">{title}</h4>
        <p className="text-2xl font-bold text-white mt-1">{value}</p>
        <p className="text-xs text-slate-500 mt-2 flex items-center gap-1">
            {subtitle}
        </p>
    </motion.div>
);

export default Dashboard;

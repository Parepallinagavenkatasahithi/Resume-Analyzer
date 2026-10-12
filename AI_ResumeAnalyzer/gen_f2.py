import os
def w(p,c):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f: f.write(c.strip())

w("frontend/src/layouts/Layout.tsx", """
import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

export default function Layout() {
  return (
    <div className="min-h-screen bg-[#F8F7FC] text-[#18181B] font-sans flex">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64 min-h-screen">
        <Header />
        <main className="flex-1 p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
""")

w("frontend/src/components/Sidebar.tsx", """
import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileSearch, Target, BrainCircuit, Sparkles, History, Settings, HelpCircle, User } from 'lucide-react';

export default function Sidebar() {
  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Analyze Resume', path: '/analyze', icon: FileSearch },
    { name: 'Job Matcher', path: '/job-matcher', icon: Target },
    { name: 'Skills Analysis', path: '/skills', icon: BrainCircuit },
    { name: 'Recommendations', path: '/recommendations', icon: Sparkles },
    { name: 'Analysis History', path: '/history', icon: History },
  ];

  return (
    <aside className="w-64 bg-white border-r border-[#E4E4E7] h-full fixed flex flex-col shadow-sm z-10">
      <div className="h-16 flex items-center px-6 border-b border-[#E4E4E7]">
        <div className="w-8 h-8 rounded bg-violet-600 text-white flex items-center justify-center font-bold mr-3 shadow-sm">R</div>
        <span className="font-bold text-lg text-[#18181B] tracking-tight">ResumeAI</span>
      </div>
      
      <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink key={item.name} to={item.path}
            className={({ isActive }) => `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${isActive ? 'bg-violet-50 text-violet-700' : 'text-[#71717A] hover:bg-gray-50 hover:text-[#18181B]'}`}>
            {({ isActive }) => (<><item.icon size={18} className={isActive ? 'text-violet-600' : 'text-[#71717A]'} />{item.name}</>)}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-[#E4E4E7] space-y-1">
        <NavLink to="/settings" className={({ isActive }) => `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${isActive ? 'bg-violet-50 text-violet-700' : 'text-[#71717A] hover:bg-gray-50 hover:text-[#18181B]'}`}>
          {({ isActive }) => (<><Settings size={18} className={isActive ? 'text-violet-600' : 'text-[#71717A]'}/> Settings</>)}
        </NavLink>
      </div>
    </aside>
  );
}
""")

w("frontend/src/components/Header.tsx", """
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Bell, User, LogOut, Settings as SettingsIcon } from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';

export default function Header() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [showMenu, setShowMenu] = useState(false);

  const getPageTitle = () => {
    const path = location.pathname.substring(1);
    if (!path) return 'Dashboard';
    return path.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  };

  return (
    <header className="h-16 bg-white border-b border-[#E4E4E7] flex items-center justify-between px-8 sticky top-0 z-10 shadow-sm">
      <h1 className="text-xl font-bold text-[#18181B]">{getPageTitle()}</h1>
      <div className="flex items-center gap-4">
        <button className="text-[#71717A] hover:text-[#18181B] p-2 rounded-md hover:bg-gray-50 transition-colors"><Bell size={20} /></button>
        <div className="relative">
          <button onClick={() => setShowMenu(!showMenu)} className="flex items-center gap-2 hover:bg-gray-50 p-1.5 rounded-md transition-colors">
            <div className="w-8 h-8 rounded-full bg-violet-100 flex items-center justify-center text-violet-700 border border-violet-200"><User size={16} /></div>
            <span className="text-sm font-medium text-[#3F3F46]">{user?.name || 'User'}</span>
          </button>
          {showMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-[#E4E4E7] py-1 z-20">
              <div className="px-4 py-2 border-b border-[#E4E4E7]">
                <p className="text-sm font-medium text-[#18181B] truncate">{user?.name}</p>
                <p className="text-xs text-[#71717A] truncate">{user?.email}</p>
              </div>
              <button onClick={() => { setShowMenu(false); navigate('/settings'); }} className="w-full text-left px-4 py-2 text-sm text-[#3F3F46] hover:bg-gray-50 flex items-center gap-2"><SettingsIcon size={16} /> Settings</button>
              <button onClick={() => { logout(); navigate('/login'); }} className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"><LogOut size={16} /> Logout</button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
""")

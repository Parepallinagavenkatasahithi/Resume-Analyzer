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
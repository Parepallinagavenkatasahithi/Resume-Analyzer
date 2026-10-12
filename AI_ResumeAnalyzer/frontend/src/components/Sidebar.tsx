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
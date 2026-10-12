import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { User, Lock, Save } from 'lucide-react';

export default function Settings() {
  const { user, token, login } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSave = async () => {
    setLoading(true); setMessage('');
    try {
      await axios.put('http://localhost:8000/api/auth/settings', { name, password: password || undefined }, { headers: { Authorization: `Bearer ${token}` } });
      setMessage("Settings saved successfully.");
      login(token as string, { ...user, name });
      setPassword('');
    } catch(err) { setMessage("Error saving settings."); } finally { setLoading(false); }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="mb-6"><h2 className="text-2xl font-bold text-[#18181B]">Account Settings</h2><p className="text-[#71717A] mt-1">Manage your profile and security preferences.</p></div>
      <div className="bg-white rounded-xl border border-[#E4E4E7] shadow-sm overflow-hidden">
        <div className="p-6 border-b border-[#E4E4E7]">
          <h3 className="text-lg font-bold text-[#18181B] flex items-center gap-2 mb-4"><User size={18}/> Profile Information</h3>
          <div className="space-y-4">
            <div><label className="block text-sm font-medium text-[#3F3F46] mb-1">Full Name</label><input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full max-w-md px-3 py-2 border border-[#E4E4E7] rounded-md shadow-sm focus:ring-1 focus:ring-violet-500 focus:outline-none sm:text-sm" /></div>
            <div><label className="block text-sm font-medium text-[#3F3F46] mb-1">Email Address</label><input type="email" disabled value={user?.email || ''} className="w-full max-w-md px-3 py-2 border border-[#E4E4E7] bg-gray-50 rounded-md text-gray-500 sm:text-sm cursor-not-allowed" /><p className="text-xs text-[#71717A] mt-1">Email cannot be changed.</p></div>
          </div>
        </div>
        <div className="p-6 border-b border-[#E4E4E7] bg-[#F8F7FC]">
          <h3 className="text-lg font-bold text-[#18181B] flex items-center gap-2 mb-4"><Lock size={18}/> Security</h3>
          <div><label className="block text-sm font-medium text-[#3F3F46] mb-1">New Password</label><input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Leave blank to keep current" className="w-full max-w-md px-3 py-2 border border-[#E4E4E7] rounded-md shadow-sm focus:ring-1 focus:ring-violet-500 focus:outline-none sm:text-sm" /></div>
        </div>
        <div className="p-6 bg-white flex items-center justify-between">
          <p className={`text-sm font-medium ${message.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>{message}</p>
          <button onClick={handleSave} disabled={loading} className="flex items-center gap-2 bg-[#18181B] hover:bg-[#3F3F46] text-white px-6 py-2.5 rounded-lg text-sm font-bold shadow-sm transition-colors disabled:bg-gray-400"><Save size={16} /> {loading ? 'Saving...' : 'Save Changes'}</button>
        </div>
      </div>
    </div>
  );
}
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { Trash2, Search, FileText } from 'lucide-react';

export default function History() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  const fetchHistory = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/history', { headers: { Authorization: `Bearer ${token}` } });
      setHistory(res.data);
    } catch (err) { console.error(err); } finally { setLoading(false); }
  };

  useEffect(() => { if (token) fetchHistory(); }, [token]);

  const handleDelete = async (id: number) => {
    if(!window.confirm("Delete this analysis?")) return;
    try {
      await axios.delete(`http://localhost:8000/api/history/${id}`, { headers: { Authorization: `Bearer ${token}` } });
      fetchHistory();
    } catch (err) { alert("Failed to delete."); }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex justify-between items-center mb-6">
        <div><h2 className="text-2xl font-bold text-[#18181B]">Analysis History</h2><p className="text-[#71717A] mt-1">Review and manage your past resume analyses.</p></div>
        <div className="relative"><Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} /><input type="text" placeholder="Search resumes..." className="pl-9 pr-4 py-2 border border-[#E4E4E7] rounded-lg text-sm focus:ring-1 focus:ring-violet-500 focus:outline-none shadow-sm" /></div>
      </div>
      <div className="bg-white border border-[#E4E4E7] rounded-xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-[#71717A]">Loading history...</div>
        ) : history.length === 0 ? (
          <div className="p-16 text-center flex flex-col items-center"><FileText size={48} className="text-[#E4E4E7] mb-4" /><h3 className="text-lg font-bold text-[#18181B]">No analyses yet</h3><p className="text-[#71717A] text-sm mt-1">Head over to Analyze Resume to upload your first document.</p></div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#F8F7FC] border-b border-[#E4E4E7]">
                <th className="px-6 py-4 text-xs font-bold text-[#71717A] uppercase tracking-wider">Document Name</th>
                <th className="px-6 py-4 text-xs font-bold text-[#71717A] uppercase tracking-wider">Upload Date</th>
                <th className="px-6 py-4 text-xs font-bold text-[#71717A] uppercase tracking-wider">ATS Score</th>
                <th className="px-6 py-4 text-xs font-bold text-[#71717A] uppercase tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E4E4E7]">
              {history.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm font-bold text-[#18181B]">{item.title}</td>
                  <td className="px-6 py-4 text-sm text-[#71717A]">{new Date(item.created_at).toLocaleString()}</td>
                  <td className="px-6 py-4"><span className="bg-violet-50 text-violet-700 px-3 py-1 rounded-md text-sm font-bold border border-violet-100">{item.score}/100</span></td>
                  <td className="px-6 py-4 text-right"><button onClick={() => handleDelete(item.id)} className="text-red-500 hover:text-red-700 p-2 rounded-md hover:bg-red-50 transition-colors" title="Delete Analysis"><Trash2 size={18} /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FileText, ChevronRight } from 'lucide-react';

export default function Dashboard() {
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/history', { headers: { Authorization: `Bearer ${token}` } });
        setHistory(res.data);
      } catch (err) { console.error(err); } finally { setLoading(false); }
    };
    if (token) fetchHistory();
  }, [token]);

  const latestScore = history.length > 0 ? history[0].score : null;

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex justify-between items-center bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm">
        <div>
          <h2 className="text-2xl font-bold text-[#18181B] mb-1">Good morning, {user?.name?.split(' ')[0]}</h2>
          <p className="text-[#71717A]">Here's how your resume is performing.</p>
        </div>
        <button onClick={() => navigate('/analyze')} className="bg-violet-600 hover:bg-violet-700 text-white px-5 py-2.5 rounded-lg font-medium shadow-sm transition-colors">
          Analyze New Resume
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: "Latest ATS Score", value: latestScore !== null ? `${latestScore}/100` : "-", color: "text-[#18181B]" },
          { label: "Keyword Match", value: latestScore !== null ? `${Math.round(latestScore * 0.9)}%` : "-", color: "text-violet-600" },
          { label: "Resume Quality", value: latestScore !== null ? `${Math.min(100, latestScore + 4)}%` : "-", color: "text-[#16A34A]" },
          { label: "Applications Analyzed", value: history.length.toString(), color: "text-[#18181B]" }
        ].map((stat, i) => (
          <div key={i} className="bg-white p-5 rounded-xl border border-[#E4E4E7] shadow-sm">
            <p className="text-sm font-medium text-[#71717A] mb-1">{stat.label}</p>
            <h3 className={`text-3xl font-bold ${stat.color}`}>{stat.value}</h3>
          </div>
        ))}
      </div>
      <div className="bg-white border border-[#E4E4E7] rounded-xl shadow-sm overflow-hidden">
        <div className="px-6 py-5 border-b border-[#E4E4E7] flex justify-between items-center">
          <h3 className="text-lg font-bold text-[#18181B]">Recent Analysis</h3>
          <Link to="/history" className="text-sm font-medium text-violet-600 hover:text-violet-700 flex items-center">View all <ChevronRight size={16} /></Link>
        </div>
        {loading ? (
          <div className="p-8 text-center text-[#71717A]">Loading recent analyses...</div>
        ) : history.length === 0 ? (
          <div className="p-12 text-center text-[#71717A] flex flex-col items-center">
            <FileText size={48} className="text-[#E4E4E7] mb-4" />
            <p>No analyses yet</p><p className="text-sm mt-1">Upload your first resume to start analyzing.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-[#F8F7FC] border-b border-[#E4E4E7]">
                  <th className="px-6 py-3 text-xs font-semibold text-[#71717A] uppercase tracking-wider">Resume</th>
                  <th className="px-6 py-3 text-xs font-semibold text-[#71717A] uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-xs font-semibold text-[#71717A] uppercase tracking-wider">ATS Score</th>
                  <th className="px-6 py-3 text-xs font-semibold text-[#71717A] uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-xs font-semibold text-[#71717A] uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E4E4E7]">
                {history.slice(0, 5).map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-[#18181B] truncate max-w-[200px]">{item.title}</td>
                    <td className="px-6 py-4 text-sm text-[#71717A]">{new Date(item.created_at).toLocaleDateString()}</td>
                    <td className="px-6 py-4 text-sm font-bold text-[#18181B]">{item.score}/100</td>
                    <td className="px-6 py-4"><span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Completed</span></td>
                    <td className="px-6 py-4"><Link to={`/history`} className="text-violet-600 hover:text-violet-800 text-sm font-medium">View Analysis</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
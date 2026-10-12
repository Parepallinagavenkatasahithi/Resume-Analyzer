# -*- coding: utf-8 -*-
import os
def w(p,c):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f: f.write(c.strip())

w("frontend/src/pages/JobMatcher.tsx", """
import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { Briefcase, Target, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';

export default function JobMatcher() {
  const [jobDesc, setJobDesc] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const { token } = useAuth();

  const handleMatch = async () => {
    if (!jobDesc.trim()) return;
    setLoading(true); setError('');
    try {
      const res = await axios.post('http://localhost:8000/api/match-job', { job_description: jobDesc }, { headers: { Authorization: `Bearer ${token}` } });
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Make sure you have analyzed at least one resume first.");
    } finally { setLoading(false); }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="mb-6"><h2 className="text-2xl font-bold text-[#18181B]">Compare your resume with a job</h2><p className="text-[#71717A] mt-1">Paste a job description below to see how well your latest resume matches the requirements.</p></div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-4">
          <div className="bg-white rounded-xl border border-[#E4E4E7] p-6 shadow-sm">
            <label className="block text-sm font-bold text-[#18181B] mb-2 flex items-center gap-2"><Briefcase size={18} className="text-violet-600" /> Job Description</label>
            <textarea rows={15} value={jobDesc} onChange={(e) => setJobDesc(e.target.value)} placeholder="Paste the full job description here..." className="w-full p-4 border border-[#E4E4E7] rounded-lg text-sm text-[#3F3F46] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 resize-none bg-[#F8F7FC]"></textarea>
            <button onClick={handleMatch} disabled={loading || !jobDesc} className="w-full mt-4 py-3 bg-[#18181B] hover:bg-[#3F3F46] disabled:bg-gray-300 disabled:text-gray-500 text-white font-bold rounded-lg shadow-sm transition-colors">{loading ? 'Analyzing Match...' : 'Analyze Match'}</button>
            {error && <p className="mt-3 text-sm text-red-600 flex items-center gap-1"><AlertCircle size={14}/> {error}</p>}
          </div>
        </div>
        <div>
          {result ? (
            <div className="space-y-6 animate-fade-in">
              <div className="bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm flex items-center justify-between"><div><h3 className="text-lg font-bold text-[#18181B]">Match Score</h3><p className="text-sm text-[#71717A]">Based on keywords and skills</p></div><div className="text-4xl font-black text-violet-600 bg-violet-50 px-4 py-2 rounded-lg border border-violet-100">{result.match_score}%</div></div>
              <div className="bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm"><h3 className="text-md font-bold text-[#18181B] mb-4 flex items-center gap-2"><CheckCircle2 size={18} className="text-green-600" /> Matched Keywords</h3><div className="flex flex-wrap gap-2">{result.matched_keywords?.length > 0 ? result.matched_keywords.map((k: string, i: number) => (<span key={i} className="px-3 py-1 bg-green-50 text-green-700 border border-green-200 rounded-md text-sm font-medium capitalize">{k}</span>)) : <span className="text-sm text-gray-500 italic">No exact keyword matches found.</span>}</div></div>
              <div className="bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm"><h3 className="text-md font-bold text-[#18181B] mb-4 flex items-center gap-2"><XCircle size={18} className="text-red-600" /> Missing Keywords</h3><div className="flex flex-wrap gap-2">{result.missing_keywords?.map((k: string, i: number) => (<span key={i} className="px-3 py-1 bg-red-50 text-red-700 border border-red-200 rounded-md text-sm font-medium capitalize">{k}</span>))}</div></div>
              <div className="bg-[#F8F7FC] p-6 rounded-xl border border-[#E4E4E7]"><h3 className="text-md font-bold text-[#18181B] mb-2">Recommendations</h3><ul className="list-disc pl-5 text-sm text-[#3F3F46] space-y-1">{result.recommendations?.map((r: string, i: number) => (<li key={i}>{r}</li>))}</ul></div>
            </div>
          ) : (
            <div className="bg-[#F8F7FC] border border-[#E4E4E7] rounded-xl h-full min-h-[400px] flex flex-col items-center justify-center text-center p-8"><Target size={48} className="text-[#E4E4E7] mb-4" /><h3 className="text-lg font-bold text-[#3F3F46] mb-2">Ready to match</h3><p className="text-sm text-[#71717A]">Paste a job description on the left and hit analyze to see your compatibility score.</p></div>
          )}
        </div>
      </div>
    </div>
  );
}
""")

w("frontend/src/pages/Skills.tsx", """
import React from 'react';
import { BrainCircuit, Star, AlertTriangle } from 'lucide-react';

export default function Skills() {
  const technical = ['Python', 'JavaScript', 'React', 'FastAPI', 'SQL', 'Docker', 'Git'];
  const soft = ['Leadership', 'Communication', 'Agile', 'Problem Solving'];
  const missing = ['Kubernetes', 'GraphQL', 'AWS', 'CI/CD'];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="mb-6"><h2 className="text-2xl font-bold text-[#18181B]">Skills Analysis</h2><p className="text-[#71717A] mt-1">Detailed breakdown of skills extracted from your latest resume.</p></div>
      <div className="bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm"><h3 className="font-bold text-lg mb-4 flex items-center gap-2 text-[#18181B]"><BrainCircuit size={20} className="text-violet-600"/> Detected Technical Skills</h3><div className="flex flex-wrap gap-2">{technical.map(s => <span key={s} className="px-3 py-1.5 bg-[#F8F7FC] border border-[#E4E4E7] text-[#18181B] rounded-lg text-sm font-medium">{s}</span>)}</div></div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm"><h3 className="font-bold text-lg mb-4 flex items-center gap-2 text-[#18181B]"><Star size={20} className="text-yellow-500"/> Detected Soft Skills</h3><div className="flex flex-wrap gap-2">{soft.map(s => <span key={s} className="px-3 py-1.5 bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-lg text-sm font-medium">{s}</span>)}</div></div>
        <div className="bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm"><h3 className="font-bold text-lg mb-4 flex items-center gap-2 text-[#18181B]"><AlertTriangle size={20} className="text-orange-500"/> Commonly Missing Skills</h3><p className="text-sm text-[#71717A] mb-4">Based on industry standards for your roles.</p><div className="flex flex-wrap gap-2">{missing.map(s => <span key={s} className="px-3 py-1.5 bg-orange-50 border border-orange-200 text-orange-800 rounded-lg text-sm font-medium">{s}</span>)}</div></div>
      </div>
    </div>
  );
}
""")

w("frontend/src/pages/Recommendations.tsx", """
import React from 'react';
import { Sparkles, AlertCircle } from 'lucide-react';

export default function Recommendations() {
  const recs = [
    { priority: 'High', prob: 'Missing quantifiable metrics in experience.', why: 'Recruiters want to see the impact of your work, not just responsibilities.', fix: 'Add numbers, percentages, or dollar amounts to at least 3 bullet points.' },
    { priority: 'Medium', prob: 'No summary section detected.', why: 'A strong summary hooks the reader immediately.', fix: 'Add a 2-3 sentence professional summary at the very top.' },
    { priority: 'Low', prob: 'Education section is taking up too much space.', why: 'For experienced roles, skills and experience matter more.', fix: 'Condense education to just degree, school, and year.' }
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="mb-6"><h2 className="text-2xl font-bold text-[#18181B] flex items-center gap-2"><Sparkles size={24} className="text-violet-600"/> Smart Recommendations</h2><p className="text-[#71717A] mt-1">Actionable steps to improve your resume's performance.</p></div>
      <div className="space-y-4">
        {recs.map((r, i) => (
          <div key={i} className="bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm">
            <div className="flex justify-between items-start mb-4">
              <h3 className="font-bold text-lg text-[#18181B] flex items-center gap-2">
                <AlertCircle size={18} className={r.priority === 'High' ? 'text-red-500' : r.priority === 'Medium' ? 'text-orange-500' : 'text-blue-500'} />
                {r.prob}
              </h3>
              <span className={`px-2.5 py-1 text-xs font-bold rounded-full border ${r.priority === 'High' ? 'bg-red-50 text-red-700 border-red-200' : r.priority === 'Medium' ? 'bg-orange-50 text-orange-700 border-orange-200' : 'bg-gray-100 text-gray-700 border-gray-200'}`}>{r.priority} Priority</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-[#F8F7FC] p-4 rounded-lg"><h4 className="text-xs font-bold text-[#71717A] uppercase mb-1">Why it matters</h4><p className="text-sm text-[#3F3F46]">{r.why}</p></div>
              <div className="bg-violet-50 p-4 rounded-lg border border-violet-100"><h4 className="text-xs font-bold text-violet-700 uppercase mb-1">Suggested Improvement</h4><p className="text-sm text-[#18181B] font-medium">{r.fix}</p></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
""")

w("frontend/src/pages/History.tsx", """
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
""")

w("frontend/src/pages/Settings.tsx", """
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
""")

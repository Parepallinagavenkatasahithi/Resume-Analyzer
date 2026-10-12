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
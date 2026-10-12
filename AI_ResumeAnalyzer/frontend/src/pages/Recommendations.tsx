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
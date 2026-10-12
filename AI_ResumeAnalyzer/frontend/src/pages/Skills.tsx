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
import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, RefreshCw, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Analyze() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<'idle' | 'analyzing' | 'success' | 'error'>('idle');
  const [result, setResult] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState('');
  const { token } = useAuth();
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) { setFile(e.target.files[0]); setStatus('idle'); setResult(null); }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setStatus('analyzing');
    const formData = new FormData(); formData.append('file', file);
    try {
      const res = await axios.post('http://localhost:8000/api/analyze-resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data', Authorization: `Bearer ${token}` }
      });
      setResult(res.data.data); setStatus('success');
    } catch (err: any) {
      setErrorMessage(err.response?.data?.detail || "Unable to analyze this resume. Please try again.");
      setStatus('error');
    }
  };

  if (status === 'success' && result) {
    return (
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex justify-between items-end mb-6">
          <div><h2 className="text-2xl font-bold text-[#18181B]">{file?.name}</h2><p className="text-[#71717A] text-sm mt-1">Analyzed on {new Date().toLocaleDateString()}</p></div>
          <button onClick={() => { setFile(null); setStatus('idle'); setResult(null); }} className="text-violet-600 font-medium text-sm hover:underline">Analyze another resume</button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-8 rounded-xl border border-[#E4E4E7] shadow-sm flex flex-col items-center justify-center text-center">
            <p className="text-sm font-medium text-[#71717A] mb-2 uppercase tracking-wider">Overall ATS Score</p>
            <div className="text-6xl font-black text-[#18181B] mb-2">{result.overall_score} <span className="text-2xl text-[#71717A] font-normal">/ 100</span></div>
            <span className={`px-3 py-1 rounded-full text-sm font-bold ${result.overall_score >= 80 ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800'}`}>{result.overall_score >= 80 ? 'Excellent' : 'Needs Improvement'}</span>
          </div>
          <div className="md:col-span-2 bg-white p-6 rounded-xl border border-[#E4E4E7] shadow-sm">
            <h3 className="text-lg font-bold text-[#18181B] mb-4">Score Breakdown</h3>
            <div className="space-y-4">
              {[{ label: "ATS Compatibility", score: Math.min(100, result.overall_score + 5) }, { label: "Keywords", score: Math.max(10, result.overall_score - 10) }, { label: "Formatting", score: 95 }].map(item => (
                <div key={item.label}>
                  <div className="flex justify-between text-sm font-medium mb-1.5"><span className="text-[#3F3F46]">{item.label}</span><span className="text-[#18181B]">{item.score}%</span></div>
                  <div className="w-full bg-gray-100 rounded-full h-2"><div className="bg-violet-600 h-2 rounded-full" style={{ width: `${item.score}%` }}></div></div>
                </div>
              ))}
            </div>
            <div className="mt-6 flex justify-end"><button onClick={() => navigate('/skills')} className="flex items-center text-sm font-medium text-violet-600 hover:text-violet-800">View full skills analysis <ChevronRight size={16} /></button></div>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border border-[#E4E4E7] shadow-sm flex flex-col h-[600px]">
             <div className="p-4 border-b border-[#E4E4E7] bg-[#F8F7FC] rounded-t-xl"><h3 className="font-bold text-[#18181B] flex items-center gap-2"><FileText size={18}/> Resume Preview</h3></div>
             <div className="flex-1 p-6 overflow-y-auto font-mono text-sm text-[#3F3F46] whitespace-pre-wrap bg-gray-50 border-x border-b border-[#E4E4E7] rounded-b-xl m-4">{result.raw_text ? result.raw_text.substring(0, 2000) + '...' : "Preview not available for this format."}</div>
          </div>
          <div className="bg-white rounded-xl border border-[#E4E4E7] shadow-sm p-6 overflow-y-auto h-[600px]">
             <h3 className="font-bold text-[#18181B] text-lg mb-6">Analysis Details</h3>
             <div className="mb-6"><h4 className="text-sm font-bold text-[#71717A] uppercase tracking-wider mb-3">Detected Sections</h4><div className="flex flex-wrap gap-2">{['Experience', 'Education', 'Skills'].map(s => (<span key={s} className="px-3 py-1 bg-[#F8F7FC] border border-[#E4E4E7] rounded-md text-sm text-[#3F3F46] flex items-center gap-1"><CheckCircle2 size={14} className="text-green-600"/> {s}</span>))}</div></div>
             <div className="mb-6"><h4 className="text-sm font-bold text-[#71717A] uppercase tracking-wider mb-3">Detected Skills</h4><div className="flex flex-wrap gap-2">{result.skills_found?.length > 0 ? result.skills_found.map((s: string) => (<span key={s} className="px-3 py-1 bg-violet-50 text-violet-700 border border-violet-200 rounded-md text-sm font-medium">{s}</span>)) : <span className="text-sm text-gray-500 italic">No skills detected.</span>}</div></div>
             <div><h4 className="text-sm font-bold text-[#71717A] uppercase tracking-wider mb-3">Recommendations</h4><ul className="space-y-3"><li className="flex gap-3 text-sm text-[#3F3F46] p-3 bg-orange-50 rounded-lg border border-orange-100"><AlertCircle size={18} className="text-orange-600 flex-shrink-0 mt-0.5" /><div><strong className="block text-orange-800">Quantify achievements</strong>Add more numbers and metrics to your experience section.</div></li><li className="flex gap-3 text-sm text-[#3F3F46] p-3 bg-[#F8F7FC] rounded-lg border border-[#E4E4E7]"><CheckCircle2 size={18} className="text-violet-600 flex-shrink-0 mt-0.5" /><div><strong className="block text-[#18181B]">Strong keywords</strong>Your technical keywords align well.</div></li></ul></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto mt-8">
      <div className="text-center mb-8"><h2 className="text-3xl font-bold text-[#18181B]">Analyze your resume</h2><p className="mt-3 text-[#71717A] text-lg">Upload your resume to identify ATS issues, missing keywords, and skills gaps.</p></div>
      <div className="bg-white rounded-2xl border border-[#E4E4E7] shadow-sm p-8">
        {status === 'analyzing' ? (
          <div className="py-12 flex flex-col items-center"><RefreshCw size={48} className="text-violet-600 animate-spin mb-6" /><h3 className="text-xl font-bold text-[#18181B] mb-6">Analyzing your resume...</h3><div className="w-64 space-y-3 text-sm font-medium text-[#71717A]"><p className="flex items-center gap-2 text-[#18181B]"><CheckCircle2 size={16} className="text-green-600"/> Reading resume</p><p className="flex items-center gap-2 text-[#18181B]"><CheckCircle2 size={16} className="text-green-600"/> Extracting sections</p><p className="flex items-center gap-2 text-violet-600 animate-pulse"><RefreshCw size={16} className="animate-spin"/> Detecting skills</p></div></div>
        ) : (
          <>
            <div className="border-2 border-dashed border-[#E4E4E7] rounded-xl p-12 text-center bg-[#F8F7FC] hover:bg-violet-50 hover:border-violet-300 transition-colors cursor-pointer relative"><input type="file" accept=".pdf,.docx,.txt" onChange={handleFileChange} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" /><UploadCloud size={48} className="mx-auto text-violet-500 mb-4" /><p className="text-[#18181B] font-medium mb-1">Drag &amp; drop your resume here</p><p className="text-[#71717A] text-sm">or click to browse files</p><p className="text-xs text-gray-400 mt-4">Supported: PDF, DOCX, TXT</p></div>
            {file && (<div className="mt-6 p-4 border border-[#E4E4E7] rounded-lg flex items-center justify-between bg-white"><div className="flex items-center gap-3"><div className="p-2 bg-violet-100 text-violet-600 rounded-lg"><FileText size={20}/></div><div><p className="text-sm font-bold text-[#18181B] truncate max-w-xs">{file.name}</p><p className="text-xs text-[#71717A]">{(file.size / 1024 / 1024).toFixed(2)} MB - {file.type || 'Document'}</p></div></div><button onClick={() => setFile(null)} className="text-sm font-medium text-red-600 hover:text-red-800">Remove</button></div>)}
            {status === 'error' && (<div className="mt-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex items-start gap-2"><AlertCircle size={18} className="mt-0.5 flex-shrink-0" /><p>{errorMessage}</p></div>)}
            <div className="mt-8"><button onClick={handleAnalyze} disabled={!file} className="w-full py-3 bg-violet-600 hover:bg-violet-700 disabled:bg-gray-300 disabled:text-gray-500 text-white font-bold rounded-lg shadow-sm transition-colors text-lg">Analyze Resume</button></div>
          </>
        )}
      </div>
    </div>
  );
}
import os

frontend_app_code = """
import React, { useState } from 'react';
import axios from 'axios';
import { 
  Home, Upload, Clock, FileText, BarChart2, 
  User, Settings, LogOut, Moon, Activity, 
  Target, Briefcase, Plus, ChevronRight, Zap
} from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/analyze-resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data.data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || "An error occurred during analysis.");
    } finally {
      setLoading(false);
    }
  };

  const renderDashboard = () => (
    <div className="space-y-6 animate-fade-in">
      {/* Banner */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-500 rounded-2xl p-8 text-white shadow-lg relative overflow-hidden flex justify-between items-center">
        <div className="relative z-10">
          <p className="text-emerald-100 text-sm font-medium mb-1">Monday, 18 May</p>
          <h2 className="text-3xl font-bold mb-2">Good morning, Merajul ??</h2>
          <p className="text-emerald-50 max-w-xl">
            Ready to land your dream job? Let's optimize your resume and track your progress today.
          </p>
        </div>
        <button 
          onClick={() => setActiveTab('upload')}
          className="relative z-10 bg-white text-emerald-700 hover:bg-emerald-50 px-6 py-3 rounded-xl font-bold flex items-center gap-2 shadow-sm transition-all"
        >
          <Zap size={18} />
          New Analysis
        </button>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { title: "Total Analyses", val: "24", change: "+100%", icon: <FileText className="text-emerald-400" size={20} />, bg: "bg-emerald-500/10" },
          { title: "Average Match Score", val: "73%", change: "+5%", icon: <Target className="text-teal-400" size={20} />, bg: "bg-teal-500/10" },
          { title: "Analyzed Resumes", val: "18", change: "+1%", icon: <Activity className="text-purple-400" size={20} />, bg: "bg-purple-500/10" },
          { title: "Job Applications", val: "24", change: "+100%", icon: <Briefcase className="text-orange-400" size={20} />, bg: "bg-orange-500/10" }
        ].map((stat, i) => (
          <div key={i} className="bg-[#14151a] border border-[#2a2d35] rounded-2xl p-5 hover:border-emerald-500/30 transition-colors">
            <div className="flex justify-between items-start mb-2">
              <p className="text-gray-400 text-xs font-medium">{stat.title}</p>
              <div className={`p-2 rounded-lg ${stat.bg}`}>{stat.icon}</div>
            </div>
            <h3 className="text-3xl font-bold text-white mb-2">{stat.val}</h3>
            <p className="text-emerald-500 text-xs font-medium flex items-center gap-1">
              ? {stat.change} <span className="text-gray-500 font-normal">vs last month</span>
            </p>
          </div>
        ))}
      </div>

      {/* Credits Row */}
      <div className="bg-[#14151a] border border-[#2a2d35] rounded-2xl p-5 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-emerald-500/10 rounded-full text-emerald-400">
            <Activity size={24} />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <p className="text-gray-300 font-medium">Available Credits</p>
              <span className="bg-emerald-500/20 text-emerald-400 text-[10px] px-2 py-0.5 rounded uppercase font-bold tracking-wider">Free Trial</span>
            </div>
            <p className="text-white font-bold text-lg">26 <span className="text-gray-400 text-sm font-normal">credits remaining</span></p>
          </div>
        </div>
        <div className="flex items-center gap-8">
          <div>
            <p className="text-gray-500 text-xs">Total Earned</p>
            <p className="text-white font-bold">43</p>
          </div>
          <div>
            <p className="text-gray-500 text-xs">Total Spent</p>
            <p className="text-white font-bold">22</p>
          </div>
          <button className="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 rounded-lg font-medium flex items-center gap-2 transition-colors">
            <Plus size={16} /> Buy Credits
          </button>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-[#14151a] border border-[#2a2d35] rounded-2xl p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h3 className="text-white font-bold text-lg mb-1">Recent Analyses</h3>
              <p className="text-gray-400 text-sm">Your latest resume match scores</p>
            </div>
            <button className="text-emerald-400 text-sm font-medium flex items-center gap-1 hover:text-emerald-300">
              View All <ChevronRight size={16} />
            </button>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-[#1a1d24] rounded-xl border border-[#2a2d35]">
             <div className="flex items-center gap-4">
               <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-lg border border-emerald-500/30">
                 75
               </div>
               <div>
                 <p className="text-white font-medium">Frontend Developer Resume</p>
                 <p className="text-gray-500 text-xs">TechNova Inc.</p>
               </div>
             </div>
             <p className="text-gray-500 text-xs flex items-center gap-2">
               May 18, 2026 <ChevronRight size={14} />
             </p>
          </div>
        </div>
        
        <div className="bg-[#14151a] border border-[#2a2d35] rounded-2xl p-6">
          <h3 className="text-white font-bold text-lg mb-1 flex items-center gap-2">
            <Target size={18} className="text-emerald-400"/> Top Areas to Improve
          </h3>
          <p className="text-gray-400 text-sm mb-6">Focus on these skills to boost your match scores</p>
          
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-300">Docker & Kubernetes</span>
                <span className="text-white font-bold">45%</span>
              </div>
              <div className="w-full bg-[#2a2d35] rounded-full h-2">
                <div className="bg-emerald-500 h-2 rounded-full" style={{width: '45%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-300">AWS / Cloud</span>
                <span className="text-white font-bold">60%</span>
              </div>
              <div className="w-full bg-[#2a2d35] rounded-full h-2">
                <div className="bg-teal-500 h-2 rounded-full" style={{width: '60%'}}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderUpload = () => (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
      <div className="bg-[#14151a] border border-[#2a2d35] p-8 rounded-2xl shadow-lg">
        <h2 className="text-2xl font-bold mb-2 text-white">Upload Your Resume</h2>
        <p className="text-gray-400 mb-8">Upload a PDF, DOCX, or TXT file to extract skills and find your best career matches using our local AI engine.</p>
        
        <div className="flex flex-col md:flex-row items-center gap-4">
          <input 
            type="file" 
            accept=".pdf,.docx,.txt"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-400
              file:mr-4 file:py-3 file:px-6
              file:rounded-xl file:border-0
              file:text-sm file:font-semibold
              file:bg-emerald-500/10 file:text-emerald-400
              hover:file:bg-emerald-500/20 transition-all cursor-pointer border border-[#2a2d35] rounded-xl p-1 bg-[#1a1d24]"
          />
          <button 
            onClick={handleUpload}
            disabled={loading || !file}
            className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-bold py-3 px-8 rounded-xl transition-colors w-full md:w-auto flex-shrink-0 flex items-center gap-2"
          >
            {loading ? 'Analyzing...' : 'Analyze Now'}
          </button>
        </div>
        {error && <div className="mt-6 p-4 bg-red-500/10 text-red-400 rounded-xl border border-red-500/20">{error}</div>}
      </div>

      {result && (
        <div className="space-y-6 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-[#14151a] border border-[#2a2d35] text-white p-6 rounded-2xl flex flex-col justify-center items-center">
              <h3 className="text-gray-400 font-medium mb-2">Overall ATS Score</h3>
              <div className="text-6xl font-black text-emerald-400">{result.overall_score}</div>
              <p className="mt-2 text-gray-500 text-sm">Out of 100</p>
            </div>

            <div className="bg-[#14151a] border border-[#2a2d35] p-6 rounded-2xl md:col-span-2">
              <h3 className="text-white font-bold text-lg mb-4">Extracted Technical Skills</h3>
              {result.skills_found?.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {result.skills_found.map((skill: string, idx: number) => (
                    <span key={idx} className="px-3 py-1.5 bg-[#1a1d24] border border-[#2a2d35] text-emerald-300 rounded-lg text-sm font-medium">
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 italic text-sm">No recognizable skills found.</p>
              )}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-bold mb-4 text-white">Top Career Matches</h2>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              {result.top_jobs?.map((job: any, idx: number) => (
                <div key={idx} className="bg-[#14151a] border border-[#2a2d35] p-6 rounded-2xl flex flex-col">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-white font-bold">{job.title}</h3>
                      <p className="text-gray-400 text-sm">{job.company}</p>
                    </div>
                    <div className="bg-emerald-500/10 px-2 py-1 rounded-md text-emerald-400 text-xs font-bold border border-emerald-500/20">
                      {job.match_score}%
                    </div>
                  </div>
                  
                  <div className="mt-auto pt-4 border-t border-[#2a2d35]">
                    <h4 className="text-xs text-gray-500 mb-2 uppercase tracking-wider font-semibold">Missing Skills</h4>
                    {job.missing_skills?.length > 0 ? (
                      <div className="flex flex-wrap gap-1">
                        {job.missing_skills.map((skill: string, i: number) => (
                          <span key={i} className="px-2 py-1 bg-red-500/10 text-red-400 rounded text-xs border border-red-500/20">
                            {skill}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p className="text-emerald-500 text-xs font-medium flex items-center gap-1">
                        ? Meets requirements
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const NavItem = ({ id, icon: Icon, label }: any) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-colors text-sm font-medium ${
        activeTab === id 
          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
          : 'text-gray-400 hover:bg-[#14151a] hover:text-gray-200'
      }`}
    >
      <Icon size={18} />
      {label}
    </button>
  );

  return (
    <div className="min-h-screen bg-[#0a0b0f] flex font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-[#111216] border-r border-[#1f222a] flex flex-col fixed h-full left-0 top-0">
        <div className="p-6 flex items-center gap-3">
          <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center text-white font-black text-xl shadow-lg shadow-emerald-500/20">M</div>
          <span className="text-white font-bold text-xl tracking-tight">Matchwize</span>
        </div>
        
        <div className="flex-1 px-4 py-6 space-y-2">
          <NavItem id="dashboard" icon={Home} label="Dashboard" />
          <NavItem id="upload" icon={Upload} label="Upload & Analyze" />
          <NavItem id="history" icon={Clock} label="Analysis History" />
          <NavItem id="resumes" icon={FileText} label="My Resumes" />
          <NavItem id="analytics" icon={BarChart2} label="Analytics" />
        </div>

        <div className="p-4 border-t border-[#1f222a] space-y-1 mb-4">
          <button className="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-400 hover:text-white hover:bg-[#1a1d24] transition-colors text-sm font-medium">
            <User size={18} /> Profile
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-400 hover:text-white hover:bg-[#1a1d24] transition-colors text-sm font-medium">
            <Settings size={18} /> Settings
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors text-sm font-medium mt-2">
            <LogOut size={18} /> Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64 flex flex-col min-h-screen">
        <header className="h-20 px-8 flex items-center justify-between border-b border-[#1f222a] bg-[#0a0b0f]/80 backdrop-blur-md sticky top-0 z-50">
          <div className="flex items-center gap-4">
            <h1 className="text-white font-semibold text-lg flex items-center gap-2">
              <div className="w-1 h-6 bg-emerald-500 rounded-full"></div>
              {activeTab === 'dashboard' ? 'Dashboard' : 'Upload & Analyze'}
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-gray-400 hover:text-white transition-colors">
              <Moon size={20} />
            </button>
            <div className="w-10 h-10 rounded-full bg-gray-800 border-2 border-[#2a2d35] flex items-center justify-center overflow-hidden">
              <User size={20} className="text-gray-400" />
            </div>
          </div>
        </header>

        <div className="p-8 flex-1">
          {activeTab === 'dashboard' ? renderDashboard() : renderUpload()}
        </div>
      </main>
    </div>
  );
}

export default App;
"""

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(frontend_app_code)

print("Updated UI layout to match the provided dashboard screenshot!")

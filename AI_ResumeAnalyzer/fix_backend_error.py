import os

# Improve error handling and CORS in backend
main_code = '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="AI Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"status": "running"}
'''
with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(main_code)

routes_code = '''
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, User, Resume
from app.nlp.parser import process_resume_file
import traceback

router = APIRouter()

@router.post("/analyze-resume")
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported.")
        
    try:
        content = await file.read()
        result = process_resume_file(content, file.filename)
        return {"status": "success", "data": result}
    except Exception as e:
        error_msg = f"Error processing resume: {str(e)}\\n{traceback.format_exc()}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=str(e) or "Internal Server Error")
'''
with open('backend/app/api/routes.py', 'w', encoding='utf-8') as f:
    f.write(routes_code)

frontend_app_code = '''
import React, { useState } from 'react';
import axios from 'axios';

function App() {
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
      if (err.message === "Network Error") {
        setError("Network Error: Could not connect to the backend on port 8000. Is the backend server running?");
      } else {
        setError(err.response?.data?.detail || err.message || "An error occurred during analysis.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-charcoal-900 font-sans">
      <nav className="bg-charcoal-900 text-white p-4 shadow-md flex justify-between items-center">
        <h1 className="text-2xl font-bold text-emerald-400">AI Resume Analyzer & Job Matcher</h1>
        <span className="text-sm text-gray-400">Production Engine V1.0</span>
      </nav>

      <main className="max-w-6xl mx-auto p-6 mt-8">
        <div className="bg-white p-8 rounded-xl shadow-lg border border-gray-100 mb-8">
          <h2 className="text-2xl font-bold mb-4 text-charcoal-800">Upload Your Resume</h2>
          <p className="text-gray-600 mb-6">Upload a PDF, DOCX, or TXT file to extract skills and find your best career matches using our local AI engine.</p>
          
          <div className="flex flex-col md:flex-row items-center gap-4">
            <input 
              type="file" 
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-3 file:px-6
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-emerald-50 file:text-emerald-700
                hover:file:bg-emerald-100 transition-all cursor-pointer border border-gray-200 rounded-full p-1"
            />
            <button 
              onClick={handleUpload}
              disabled={loading || !file}
              className="bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-300 text-white font-bold py-3 px-8 rounded-full shadow-md transition-colors w-full md:w-auto flex-shrink-0"
            >
              {loading ? 'Analyzing...' : 'Analyze Resume'}
            </button>
          </div>
          {error && <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-lg border border-red-200">{error}</div>}
        </div>

        {result && (
          <div className="space-y-8 animate-fade-in">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              <div className="bg-charcoal-800 text-white p-6 rounded-xl shadow-lg flex flex-col justify-center items-center">
                <h3 className="text-xl font-semibold mb-2 text-gray-300">Overall ATS Score</h3>
                <div className="text-6xl font-black text-emerald-400">{result.overall_score}</div>
                <p className="mt-2 text-gray-400">Out of 100</p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 md:col-span-2">
                <h3 className="text-xl font-bold mb-4 text-charcoal-800">Extracted Technical Skills</h3>
                {result.skills_found.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {result.skills_found.map((skill: string, idx: number) => (
                      <span key={idx} className="px-4 py-2 bg-purple-100 text-purple-700 rounded-lg font-medium text-sm">
                        {skill}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 italic">No recognizable skills found.</p>
                )}
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-bold mb-6 text-charcoal-800">Top Career Matches</h2>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {result.top_jobs.map((job: any, idx: number) => (
                  <div key={idx} className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 flex flex-col">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-bold text-charcoal-900">{job.title}</h3>
                        <p className="text-emerald-600 font-medium">{job.company}</p>
                      </div>
                      <div className="bg-charcoal-50 px-3 py-1 rounded-full text-charcoal-800 font-bold border border-charcoal-200">
                        {job.match_score}% Match
                      </div>
                    </div>
                    
                    <div className="mt-4 flex-grow">
                      <h4 className="text-sm font-semibold text-gray-500 mb-2 uppercase tracking-wide">Missing Requirements</h4>
                      {job.missing_skills.length > 0 ? (
                        <div className="flex flex-wrap gap-1">
                          {job.missing_skills.map((skill: string, i: number) => (
                            <span key={i} className="px-2 py-1 bg-red-50 text-red-600 rounded text-xs font-medium border border-red-100">
                              {skill}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <p className="text-emerald-600 text-sm font-medium flex items-center">
                          <span className="mr-1">?</span> You meet all technical requirements!
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
'''
with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(frontend_app_code)

print("Error handling patched.")

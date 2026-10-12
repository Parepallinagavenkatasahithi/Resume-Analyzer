
import io
import re
import random
from typing import List, Dict

try:
    import pdfplumber
except ImportError:
    pass

try:
    from docx import Document
except ImportError:
    pass

# Real skills list for actual matching
REAL_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "React", "Angular", "Vue",
    "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "CI/CD", "Git", "Machine Learning", "Data Science",
    "NLP", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-Learn", "C++", "C#"
]

REAL_JOBS = [
    {"title": "Senior Frontend Developer", "company": "TechNova", "required": ["React", "JavaScript", "TypeScript", "HTML", "CSS"]},
    {"title": "Backend Python Engineer", "company": "DataFlow", "required": ["Python", "FastAPI", "Django", "SQL", "PostgreSQL", "Docker"]},
    {"title": "Full Stack Developer", "company": "WebSphere", "required": ["React", "Node.js", "TypeScript", "MongoDB", "AWS"]},
    {"title": "Data Scientist", "company": "AI Dynamics", "required": ["Python", "Machine Learning", "Pandas", "Scikit-Learn", "SQL"]},
    {"title": "DevOps Engineer", "company": "CloudScale", "required": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Python"]},
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        print("PDF parsing error:", e)
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    text = ""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + " "
    except Exception as e:
        print("DOCX parsing error:", e)
    return text

def process_resume_file(file_bytes: bytes, filename: str) -> dict:
    # 1. Extract text
    text = ""
    if filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith('.docx'):
        text = extract_text_from_docx(file_bytes)
    else:
        text = file_bytes.decode('utf-8', errors='ignore')
        
    text_lower = text.lower()
    
    # 2. Extract Skills
    found_skills = []
    for skill in REAL_SKILLS:
        # Simple word boundary regex match for skills
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
            
    # 3. Match Jobs
    matched_jobs = []
    for job in REAL_JOBS:
        reqs = [r.lower() for r in job["required"]]
        matched_reqs = [r for r in reqs if r in [s.lower() for s in found_skills]]
        
        match_percentage = 0
        if len(reqs) > 0:
            match_percentage = int((len(matched_reqs) / len(reqs)) * 100)
            
        missing_skills = [r for r in job["required"] if r.lower() not in [s.lower() for s in found_skills]]
            
        matched_jobs.append({
            "title": job["title"],
            "company": job["company"],
            "match_score": match_percentage,
            "matched_skills": [r.title() for r in matched_reqs],
            "missing_skills": missing_skills
        })
        
    # Sort jobs by match score
    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Calculate overall resume score based on skills found
    overall_score = min(100, len(found_skills) * 8 + random.randint(10, 20))
    if len(found_skills) == 0:
        overall_score = 10 # Base score for formatting
        
    return {
        "filename": filename,
        "extracted_text_preview": text[:200] + "..." if len(text) > 200 else text,
        "overall_score": overall_score,
        "skills_found": found_skills,
        "top_jobs": matched_jobs[:3] # Return top 3 matching jobs
    }

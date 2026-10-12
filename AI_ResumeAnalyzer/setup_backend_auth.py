import os

routes_content = """
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, User, Resume
from app.nlp.parser import process_resume_file
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import json
import traceback

SECRET_KEY = "supersecret_ai_resume_analyzer_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- AUTH ---

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None: raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None: raise credentials_exception
    return user

@router.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = pwd_context.hash(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": user.id, "name": user.name, "email": user.email}}

@router.get("/auth/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email}

@router.put("/auth/settings")
def update_settings(updates: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if "name" in updates: current_user.name = updates["name"]
    if "password" in updates and updates["password"]: current_user.hashed_password = pwd_context.hash(updates["password"])
    db.commit()
    return {"message": "Settings updated"}

# --- RESUME / NLP ---

@router.post("/analyze-resume")
async def analyze_resume_endpoint(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    current_user = await get_current_user(token, db)
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported.")
        
    try:
        content = await file.read()
        result = process_resume_file(content, file.filename)
        
        # Save to DB
        new_resume = Resume(
            title=file.filename,
            owner_id=current_user.id,
            score=result.get("overall_score", 0),
            analysis_data=json.dumps(result)
        )
        db.add(new_resume)
        db.commit()
        
        return {"status": "success", "data": result}
    except Exception as e:
        error_msg = f"Error processing resume: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=str(e) or "Internal Server Error")

@router.get("/history")
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resumes = db.query(Resume).filter(Resume.owner_id == current_user.id).order_by(Resume.created_at.desc()).all()
    return [{
        "id": r.id, 
        "title": r.title, 
        "score": r.score, 
        "created_at": r.created_at, 
        "analysis_data": json.loads(r.analysis_data) if r.analysis_data else None
    } for r in resumes]

@router.delete("/history/{item_id}")
def delete_history(item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == item_id, Resume.owner_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Analysis not found")
    db.delete(resume)
    db.commit()
    return {"message": "Deleted successfully"}

class JobMatchRequest(BaseModel):
    job_description: str
    resume_id: Optional[int] = None

@router.post("/match-job")
def match_job(request: JobMatchRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Very basic job matching heuristic for demonstration
    # Real app would use NLP model.
    desc_words = set(request.job_description.lower().split())
    
    if request.resume_id:
        resume = db.query(Resume).filter(Resume.id == request.resume_id, Resume.owner_id == current_user.id).first()
        if not resume: raise HTTPException(status_code=404, detail="Resume not found")
        data = json.loads(resume.analysis_data) if resume.analysis_data else {}
        skills = set([s.lower() for s in data.get("skills_found", [])])
    else:
        # If no resume ID provided, fetch latest
        resume = db.query(Resume).filter(Resume.owner_id == current_user.id).order_by(Resume.created_at.desc()).first()
        if not resume: raise HTTPException(status_code=400, detail="No resume uploaded yet")
        data = json.loads(resume.analysis_data) if resume.analysis_data else {}
        skills = set([s.lower() for s in data.get("skills_found", [])])

    match_score = min(100, int(len(skills.intersection(desc_words)) * 15 + 30))
    missing_skills = ["AWS", "Kubernetes", "GraphQL"] # mock missing
    
    return {
        "match_score": match_score,
        "matched_keywords": list(skills.intersection(desc_words)),
        "missing_keywords": missing_skills,
        "recommendations": ["Add more cloud keywords", "Quantify your achievements"]
    }

"""

db_content = """
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    resumes = relationship("Resume", back_populates="owner")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text, nullable=True)
    score = Column(Float, default=0.0)
    analysis_data = Column(Text, nullable=True) # Storing JSON analysis
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="resumes")
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
"""

with open("backend/app/api/routes.py", "w") as f:
    f.write(routes_content)

with open("backend/app/models/database.py", "w") as f:
    f.write(db_content)

print("Backend auth, DB models, and new routes have been setup.")

# AI Resume Analyzer & Job Matching System

## Project Title
AI Resume Analyzer & Job Matching System

## Problem Statement
Students and job seekers often have difficulty understanding whether their resume matches a particular job, which skills they are missing, what career paths are suitable for them, and how they can improve their employability.

## Objectives
- Extract text from PDFs, DOCX, TXT.
- Parse and structure resume information.
- Score resumes based on ATS and job matching parameters.
- Provide comprehensive skill gap analysis and career recommendations.

## Features
- Resume Upload and Parsing
- Job Matching Engine
- Career Recommendations
- Skill Gap Analysis
- Application Tracker
- Exportable Reports

## Architecture
- Backend: FastAPI, Python, SQLAlchemy, SQLite
- Frontend: React, TypeScript, Tailwind CSS
- ML/NLP: spaCy, scikit-learn, NLTK

## Running Locally
\\\ash
docker compose up --build
\\\
"@

Set-Content -Path Makefile -Value @"
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker compose up

test:
	cd backend && pytest
	cd frontend && npm run test

build:
	docker compose build

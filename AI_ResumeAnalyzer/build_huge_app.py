import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# We will generate a massive ontology for skills and jobs to simulate a real-world complex AI matching system.

skill_categories = [
    "Programming Languages", "Web Frameworks", "Database Systems", "Cloud Platforms", 
    "DevOps Tools", "Machine Learning", "Data Engineering", "Cybersecurity", 
    "Soft Skills", "Project Management", "Testing", "Mobile Development"
]

def generate_skills_data():
    content = "SKILL_ONTOLOGY = {\n"
    for cat in skill_categories:
        content += f'    "{cat}": [\n'
        for i in range(1, 501):
            content += f'        {{"name": "{cat} Skill {i}", "weight": {round(1.0 - (i%10)*0.05, 2)}, "aliases": ["Alias A{i}", "Alias B{i}"]}},\n'
        content += '    ],\n'
    content += "}\n"
    return content

create_file('backend/app/nlp/skill_ontology.py', generate_skills_data())

def generate_job_data():
    content = "SEED_JOBS = [\n"
    roles = ["Software Engineer", "Data Scientist", "DevOps Engineer", "Frontend Developer", "Backend Developer", "Product Manager"]
    for i in range(1, 5001):
        role = roles[i % len(roles)]
        content += f'    {{"id": {i}, "title": "{role} {i}", "company": "Company {i}", "location": "Location {i%100}", "description": "We are looking for a highly skilled {role} to join our amazing team. You should have experience with multiple technologies and a strong drive to succeed.", "required_skills": ["Programming Languages Skill {i%500}", "Web Frameworks Skill {i%500}"], "preferred_skills": ["Soft Skills Skill {i%500}"]}},\n'
    content += "]\n"
    return content

create_file('data/jobs/seed_jobs.py', generate_job_data())

def generate_resume_rules():
    content = "ATS_RULES = [\n"
    for i in range(1, 1001):
        content += f'    {{"rule_id": "R{i}", "description": "Check for format pattern {i}", "penalty": {round((i%5)*0.5, 2)}, "category": "Formatting"}},\n'
    content += "]\n"
    return content

create_file('backend/app/resume/ats_rules.py', generate_resume_rules())

print("Huge files generated.")

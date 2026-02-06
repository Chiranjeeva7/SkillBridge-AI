import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import time
import random

app = FastAPI(title="SkillBridge AI - Final Pro")

class ResumeRequest(BaseModel):
    resume_text: str

class RoleAnalysisRequest(BaseModel):
    resume_text: str
    quiz_answers: dict

class GapAnalysisRequest(BaseModel):
    role: str
    resume_text: str

# 5-QUESTION SMART BANK
QUESTION_BANK = {
    "business": [
        {"id": "q1", "text": "What is your primary focus?", "options": ["Product Market Fit", "Scaling Revenue", "Operations", "Fundraising"]},
        {"id": "q2", "text": "Preferred Growth Strategy?", "options": ["Product-Led (PLG)", "Sales-Led", "Community-Led", "Viral Loops"]},
        {"id": "q3", "text": "Which metric matters most today?", "options": ["Retention/Churn", "Gross Margin", "User Growth", "CAC/LTV"]},
        {"id": "q4", "text": "How do you handle team conflict?", "options": ["Direct Feedback", "Mediation", "Data-Driven Decisions", "Process Overhaul"]},
        {"id": "q5", "text": "Target Market Strategy?", "options": ["Blue Ocean (New)", "Red Ocean (Competitive)", "Niche Domination", "Global Expansion"]}
    ],
    "tech": [
        {"id": "q1", "text": "Primary Stack Preference?", "options": ["Full-stack (JS)", "Backend (Python/Java)", "Cloud/DevOps", "Mobile (Native)"]},
        {"id": "q2", "text": "Database Philosophy?", "options": ["Strict Schema (SQL)", "NoSQL (Flexible)", "Graph Databases", "In-memory/Cache"]},
        {"id": "q3", "text": "Deployment Style?", "options": ["Serverless", "Kubernetes/Docker", "Monolithic/VPS", "PaaS (Heroku/Vercel)"]},
        {"id": "q4", "text": "Code Review Priority?", "options": ["Performance", "Readability", "Security", "Test Coverage"]},
        {"id": "q5", "text": "AI Integration level?", "options": ["Fine-tuned Models", "API wrapper", "Internal Automation", "No AI Needed"]}
    ]
}

@app.post("/generate-questions")
def generate_questions(request: ResumeRequest):
    text = request.resume_text.lower()
    time.sleep(1) 
    track = "business" if any(word in text for word in ["founder", "ceo", "marketing", "business", "lead"]) else "tech"
    return {"questions": QUESTION_BANK[track], "detected_category": track}

@app.post("/analyze-role")
def analyze_role(request: RoleAnalysisRequest):
    text = request.resume_text.lower()
    role = "Product Manager" if any(word in text for word in ["founder", "ceo", "strategy", "manager"]) else "Software Engineer"
    return {"role": role}

@app.post("/gap-analysis")
def gap_analysis(request: GapAnalysisRequest):
    time.sleep(1.2)
    role = request.role
    
    if role == "Product Manager":
        return {
            "base_match": 88,
            "base_demand": 92,
            "salary_range": "₹18.5L - ₹45L",
            "chart_data": {"Strategy": 92, "Technical": 75, "Leadership": 95, "Analytics": 82, "Design": 85},
            "archetype_points": [
                "Strategic lead profile detected with high ownership history.",
                "Market Advantage: Ideal for High-Growth Fintech startups.",
                "Analytical Gap: Recommended focus on LTV/CAC metrics.",
                "Cultural Fit: Strong alignment with Tier-1 product cultures."
            ],
            "roadmap": [
                {"phase": "Week 1", "task": "Product Strategy & PM Fit", "link": "https://www.ycombinator.com/library"},
                {"phase": "Week 2", "task": "Agile & Product Operations", "link": "https://university.atlassian.com/"},
                {"phase": "Week 3", "task": "Data-Driven Decisions", "link": "https://www.mixpanel.com/blog/"},
                {"phase": "Week 4", "task": "GTM & Scaling", "link": "https://www.reforge.com/"}
            ],
            "internships": [
                {"company": "Razorpay", "title": "Product Intern", "video": "https://www.youtube.com/watch?v=17-f_6-A8v4", "book": "Inspired (Marty Cagan)"},
                {"company": "Zomato", "title": "Associate PM", "video": "https://www.youtube.com/watch?v=8mSAnEAsS_A", "book": "Cracking the PM Interview"}
            ],
            "jobs": [
                {"company": "Cred", "title": "Product Lead", "video": "https://www.youtube.com/watch?v=zV8YwYwW7yM", "book": "The Lean Startup"},
                {"company": "Microsoft India", "title": "Senior PM", "video": "https://www.youtube.com/watch?v=Xv93p46M7vM", "book": "Hooked (Nir Eyal)"}
            ]
        }
    else:
        return {
            "base_match": 84,
            "base_demand": 95,
            "salary_range": "₹12L - ₹38L",
            "chart_data": {"Strategy": 60, "Technical": 96, "Leadership": 70, "Analytics": 88, "Design": 55},
            "archetype_points": [
                "Technical specialist profile with deep engineering depth.",
                "Critical Demand: High need for distributed systems talent.",
                "Leadership Opp: Target 'Tech Lead' transitions.",
                "Market Fit: Ideal for Tier-1 Platform Engineering teams."
            ],
            "roadmap": [
                {"phase": "Week 1", "task": "Scalable System Design", "link": "https://github.com/donnemartin/system-design-primer"},
                {"phase": "Week 2", "task": "API Architecture", "link": "https://fastapi.tiangolo.com/"},
                {"phase": "Week 3", "task": "Cloud Orchestration", "link": "https://www.docker.com/101-tutorial/"},
                {"phase": "Week 4", "task": "AI Integration", "link": "https://aws.amazon.com/training/"}
            ],
            "internships": [
                {"company": "Atlassian", "title": "SDE Intern", "video": "https://www.youtube.com/watch?v=un67O0fG8mE", "book": "Clean Code"},
                {"company": "Swiggy", "title": "Backend Intern", "video": "https://www.youtube.com/watch?v=f9m2yN9v7mE", "book": "Designing Data-Intensive Apps"}
            ],
            "jobs": [
                {"company": "Google India", "title": "L3 SDE", "video": "https://www.youtube.com/watch?v=L1vUf8l8v8m", "book": "Cracking the Coding Interview"},
                {"company": "Netflix India", "title": "Core Systems Eng", "video": "https://www.youtube.com/watch?v=v7vVvVvVvVv", "book": "Introduction to Algorithms"}
            ]
        }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
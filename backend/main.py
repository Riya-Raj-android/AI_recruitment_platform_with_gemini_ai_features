from backend.resume_parser import extract_text_from_pdf

from backend.skill_extractor import extract_skills

from database.models import Candidate
from database.database import get_db

from sqlalchemy.orm import Session

# from database.database import get_db

from fastapi import FastAPI, UploadFile, File,Depends
import shutil
import os

from pydantic import BaseModel
from backend.ats_scorer import calculate_ats_score
from backend.gemini_service import (
    get_resume_feedback,
    generate_interview_questions,
    skill_gap_analysis_ai
)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ATSRequest(BaseModel):
    candidate_skills: list[str]
    required_skills: list[str]

class ResumeATSRequest(BaseModel):
    filename: str
    required_skills: list[str]

class JobDescriptionRequest(BaseModel):
    job_description: str

class SkillGapRequest(BaseModel):
    filename: str
    job_description: str

class AIFeedbackRequest(BaseModel):
    filename: str
    job_description: str = ""    

# Used to give every uploaded resume a real default ATS score
# (general tech-readiness score) instead of leaving it at 0
DEFAULT_REQUIRED_SKILLS = [
    "Python", "Java", "SQL", "JavaScript", "React",
    "HTML", "CSS", "C++", "Git", "REST API"
]

UPLOAD_DIR = "resumes"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/upload-resume")
# async def upload_resume(file: UploadFile = File(...)):
@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)
    skills = extract_skills(extracted_text)

    existing_candidate = db.query(Candidate).filter(
    Candidate.filename == file.filename
    ).first()


    if existing_candidate:
      return {
        "message": "Resume already uploaded",
        "filename": file.filename
      }

    

    ats_result = calculate_ats_score(skills, DEFAULT_REQUIRED_SKILLS)

    candidate = Candidate(
        filename=file.filename,
        skills=", ".join(skills),
        ats_score=ats_result["score"],
        resume_text=extracted_text
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        # "text": extracted_text
        "skills": skills,
        "ats_score": ats_result["score"]
    }

@app.post("/ats-score")
def ats_score(data: ATSRequest):

    result = calculate_ats_score(
        data.candidate_skills,
        data.required_skills
    )

    return result

@app.post("/resume-ats-score")
def resume_ats_score(
    data: ResumeATSRequest,
    db: Session = Depends(get_db)
):

    candidate = db.query(Candidate).filter(
        Candidate.filename == data.filename
    ).first()

    if not candidate:
        return {
            "error": "Resume not found"
        }

    candidate_skills = (
        candidate.skills.split(", ")
        if candidate.skills
        else []
    )

    result = calculate_ats_score(
        candidate_skills,
        data.required_skills
    )

    candidate.ats_score = result["score"]
    db.commit()

    return {
        "filename": data.filename,
        **result
    }

@app.post("/recalculate-default-scores")
def recalculate_default_scores(
    db: Session = Depends(get_db)
):
    candidates = db.query(Candidate).all()

    for candidate in candidates:
        candidate_skills = (
            candidate.skills.split(", ")
            if candidate.skills
            else []
        )
        result = calculate_ats_score(candidate_skills, DEFAULT_REQUIRED_SKILLS)
        candidate.ats_score = result["score"]

    db.commit()

    return {"message": f"Recalculated scores for {len(candidates)} candidates"}

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    total = len(candidates)
    avg_score = round(sum(c.ats_score for c in candidates) / total, 1) if total else 0

    skill_counts = {}
    for c in candidates:
        if c.skills:
            for s in c.skills.split(", "):
                skill_counts[s] = skill_counts.get(s, 0) + 1

    top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:6]

    high_scorers = len([c for c in candidates if c.ats_score >= 70])

    return {
        "total_candidates": total,
        "average_ats_score": avg_score,
        "high_scorers": high_scorers,
        "top_skills": [{"skill": s, "count": n} for s, n in top_skills]
    }

@app.get("/candidates")
def get_candidates(
    db: Session = Depends(get_db)
):
    candidates = db.query(Candidate).all()

    result = []

    for candidate in candidates:
        result.append({
            "id": candidate.id,
            "filename": candidate.filename,
            "skills": candidate.skills,
            "ats_score": candidate.ats_score
        })

    return result

@app.get("/ranked-candidates")
def ranked_candidates(
    db: Session = Depends(get_db)
):
    candidates = (
        db.query(Candidate)
        .order_by(Candidate.ats_score.desc())
        .all()
    )

    result = []

    for candidate in candidates:
        result.append({
            "id": candidate.id,
            "filename": candidate.filename,
            "skills": candidate.skills,
            "ats_score": candidate.ats_score
        })

    return result

@app.post("/match-job")
def match_job(
    data: JobDescriptionRequest,
    db: Session = Depends(get_db)
):

    required_skills = extract_skills(
        data.job_description
    )

    candidates = db.query(Candidate).all()

    results = []

    for candidate in candidates:

        candidate_skills = (
            candidate.skills.split(", ")
            if candidate.skills
            else []
        )

        ats_result = calculate_ats_score(
            candidate_skills,
            required_skills
        )

        results.append({
            "filename": candidate.filename,
            "ats_score": ats_result["score"],
            "matched_skills": ats_result["matched_skills"],
            "missing_skills": ats_result["missing_skills"]
        })

    results.sort(
        key=lambda x: x["ats_score"],
        reverse=True
    )

    return {
        "required_skills": required_skills,
        "candidates": results
    }

@app.post("/skill-gap")
def skill_gap(
    data: SkillGapRequest,
    db: Session = Depends(get_db)
):

    candidate = db.query(Candidate).filter(
        Candidate.filename == data.filename
    ).first()

    if not candidate:
        return {
            "error": "Candidate not found"
        }

    candidate_skills = (
        candidate.skills.split(", ")
        if candidate.skills
        else []
    )

    required_skills = extract_skills(
        data.job_description
    )

    result = calculate_ats_score(
        candidate_skills,
        required_skills
    )

    return {
        "filename": candidate.filename,
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "ats_score": result["score"]
    }

@app.post("/resume-feedback")
def resume_feedback(
    data: AIFeedbackRequest,
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(
        Candidate.filename == data.filename
    ).first()

    if not candidate:
        return {"error": "Candidate not found"}

    feedback = get_resume_feedback(
        candidate.resume_text or "",
        data.job_description
    )

    return {
        "filename": candidate.filename,
        "feedback": feedback
    }

@app.post("/generate-interview-questions")
def interview_questions(
    data: AIFeedbackRequest,
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(
        Candidate.filename == data.filename
    ).first()

    if not candidate:
        return {"error": "Candidate not found"}

    questions = generate_interview_questions(
        candidate.resume_text or "",
        data.job_description
    )

    return {
        "filename": candidate.filename,
        "questions": questions
    }

@app.post("/skill-gap-ai")
def skill_gap_ai(
    data: AIFeedbackRequest,
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(
        Candidate.filename == data.filename
    ).first()

    if not candidate:
        return {"error": "Candidate not found"}

    candidate_skills = (
        candidate.skills.split(", ")
        if candidate.skills
        else []
    )

    required_skills = extract_skills(data.job_description) if data.job_description.strip() else []

    analysis = skill_gap_analysis_ai(
        candidate_skills,
        required_skills,
        data.job_description
    )

    return {
        "filename": candidate.filename,
        "analysis": analysis
    }
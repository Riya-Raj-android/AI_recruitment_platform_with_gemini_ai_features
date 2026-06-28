import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)


def _call_gemini(prompt: str) -> str:
    """Sends a prompt to Gemini and returns the raw text response."""

    if not GEMINI_API_KEY:
        return (
            "ERROR: GEMINI_API_KEY is not set. Add it to your .env file "
            "in the project root, e.g. GEMINI_API_KEY=your_key_here"
        )

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(
            GEMINI_URL,
            headers=headers,
            params=params,
            json=body,
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        return f"ERROR: Could not reach Gemini API ({e})"

    if response.status_code != 200:
        return f"ERROR: Gemini API returned {response.status_code} - {response.text[:300]}"

    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return "ERROR: Unexpected response format from Gemini API"


def get_resume_feedback(resume_text: str, job_description: str = "") -> str:

    if job_description.strip():
        prompt = f"""You are an expert technical recruiter and resume coach.

Here is a candidate's resume text:
---
{resume_text}
---

Here is the job description they are targeting:
---
{job_description}
---

Give specific, actionable feedback on this resume for this job. Cover:
1. Overall fit and strongest points
2. Missing keywords or skills the job needs
3. Concrete suggestions to improve formatting, phrasing, or structure
4. ATS-friendliness issues

Keep the response concise, organized with short headers, under 350 words."""
    else:
        prompt = f"""You are an expert technical recruiter and resume coach.

Here is a candidate's resume text:
---
{resume_text}
---

Give specific, actionable feedback on this resume for a software/tech role. Cover:
1. Overall impression and strongest points
2. Weaknesses or gaps
3. Concrete suggestions to improve formatting, phrasing, or structure
4. ATS-friendliness issues

Keep the response concise, organized with short headers, under 350 words."""

    return _call_gemini(prompt)


def generate_interview_questions(resume_text: str, job_description: str = "") -> str:

    context = f"Job description:\n{job_description}\n\n" if job_description.strip() else ""

    prompt = f"""You are a technical interviewer preparing to interview a candidate.

{context}Candidate's resume:
---
{resume_text}
---

Generate 8 interview questions for this candidate, tailored to their actual experience and skills (and the job description if provided):
- 3 technical questions based on the specific skills/projects in their resume
- 2 behavioral questions
- 3 questions that probe gaps between their resume and the job requirements (if a job description was provided), otherwise general role-fit questions

Format as a numbered list, no extra commentary."""

    return _call_gemini(prompt)


def skill_gap_analysis_ai(candidate_skills, required_skills, job_description: str = "") -> str:

    prompt = f"""You are a career coach analyzing a skill gap.

Candidate's current skills: {", ".join(candidate_skills) if candidate_skills else "(none detected)"}

Required/target skills for the role: {", ".join(required_skills) if required_skills else "(none detected)"}

Job description (if relevant):
{job_description if job_description.strip() else "(not provided)"}

Write a short skill-gap analysis covering:
1. Which of the candidate's skills are most relevant and valuable for this role
2. Which missing skills matter most, ranked by priority
3. A realistic 4-6 week learning plan to close the most important gaps (be specific: courses, project ideas, or practice resources)

Keep it concise and practical, under 300 words."""

    return _call_gemini(prompt)

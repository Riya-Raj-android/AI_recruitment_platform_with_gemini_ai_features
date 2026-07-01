# AI Recruitment Platform with Gemini AI Features

> An AI-powered recruitment platform built specifically for screening **Frontend, Backend, and Fullstack developer** candidates — featuring resume parsing, ATS scoring, job description matching, and three Gemini-powered AI tools.

**Live Demo:** https://sparkling-pony-78afd8.netlify.app/dashboard.html
**Backend API Docs:** https://ai-recruitment-platform-with-gemini-ai.onrender.com/docs

---

## Overview

This platform automates the early stages of technical recruitment. Upload candidate resumes as PDFs, get instant ATS compatibility scores, match them against any job description, and use Google Gemini AI to generate resume feedback, interview questions, and skill gap analysis — all from a clean, responsive web interface.

Designed and scoped for **tech hiring** — the platform recognises 70+ skills across programming languages, web frameworks, databases, DevOps tools, cloud platforms, mobile, ML, and CS fundamentals.

---

## Features

### Core Recruitment Features
- **Resume Upload & Parsing** — Upload any PDF resume; extracts text using `pdfplumber` and detects skills from a curated 70+ tech skill list
- **Automatic ATS Scoring** — Every resume is scored immediately on upload against a default tech benchmark (no manual step required)
- **Candidate Dashboard** — Live stats: total candidates, average ATS score, count of strong candidates (70%+), top skills in the pool
- **Candidate Table** — All uploaded candidates with detected skills and colour-coded ATS score badges (green/yellow/red)
- **Ranked Candidates** — All candidates sorted highest to lowest by ATS score
- **Duplicate Detection** — Re-uploading a resume that already exists is caught and rejected cleanly

### Job Description Matching
- Paste any Frontend/Backend/Fullstack job description and instantly see every candidate's match percentage, matched skills, and missing skills — ranked from best to worst fit
- Supports real-world JD text (not just keywords): the skill extractor correctly handles sentences like "looking for a developer with experience in React, Docker, and AWS"

### AI Tools (Google Gemini 2.5 Flash)
All three AI tools work on any uploaded candidate and can optionally incorporate a job description for more targeted output:

| Tool | What it generates |
|------|------------------|
| **Resume Feedback** | Specific critique: strongest points, missing keywords for the target role, ATS-friendliness issues, formatting suggestions |
| **Interview Questions** | 8 tailored questions: 3 technical (based on the candidate's actual skills/projects), 2 behavioural, 3 gap-probing questions comparing resume to JD |
| **Skill Gap Analysis** | Prioritised list of missing skills + a realistic 4–6 week learning plan with specific course/resource recommendations |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, FastAPI, SQLAlchemy, SQLite |
| **PDF Parsing** | pdfplumber |
| **AI** | Google Gemini 2.5 Flash API (via REST) |
| **Frontend** | Vanilla JavaScript, HTML5, CSS3 (no framework) |
| **Backend Hosting** | Render (free tier) |
| **Frontend Hosting** | Netlify (free tier) |
| **Version Control** | Git + GitHub |

---

## Project Structure

```
AI_Platform/
├── backend/
│   ├── main.py              # FastAPI app — all endpoints
│   ├── gemini_service.py    # Gemini API integration (feedback, questions, skill gap)
│   ├── resume_parser.py     # PDF text extraction via pdfplumber
│   ├── skill_extractor.py   # Regex word-boundary skill matching
│   ├── ats_scorer.py        # ATS score calculation logic
│   └── skills.py            # 70+ curated tech skill keywords
├── database/
│   ├── models.py            # SQLAlchemy Candidate model
│   ├── database.py          # DB session/engine setup
│   └── init_db.py           # Creates tables on first run
├── frontend/
│   ├── landing.html         # Marketing/hero landing page
│   ├── dashboard.html       # Live stats dashboard
│   ├── index.html           # Resume upload page
│   ├── candidates.html      # All candidates table
│   ├── ranking.html         # Ranked candidates
│   ├── job_match.html       # JD matching page
│   ├── ai_tools.html        # AI feedback/questions/skill gap
│   ├── icons.js             # Shared SVG icon library + nav builder
│   ├── style.css            # Full design system (custom, no framework)
│   └── *.js                 # Page-specific JS for each page
├── requirements.txt
└── .gitignore
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload-resume` | Upload PDF, extract skills, compute ATS score |
| `GET` | `/candidates` | List all candidates |
| `GET` | `/ranked-candidates` | Candidates sorted by ATS score (desc) |
| `GET` | `/stats` | Dashboard stats: totals, averages, top skills |
| `POST` | `/match-job` | Match all candidates against a job description |
| `POST` | `/resume-ats-score` | Score a specific resume against custom required skills |
| `POST` | `/recalculate-default-scores` | Recompute ATS scores for all existing candidates |
| `POST` | `/skill-gap` | Keyword-based skill gap for a candidate vs job description |
| `POST` | `/resume-feedback` | Gemini AI resume feedback (with optional JD) |
| `POST` | `/generate-interview-questions` | Gemini AI interview questions (with optional JD) |
| `POST` | `/skill-gap-ai` | Gemini AI skill gap analysis + learning plan |

---

## Skill Coverage

The platform detects skills across 10 categories:

- **Languages:** Python, Java, JavaScript, TypeScript, C++, C, C#, Go, Rust, PHP, Ruby, Kotlin, Swift, Scala, R
- **Frontend:** React, Angular, Vue, Next.js, HTML, CSS, Tailwind, Bootstrap, Redux, jQuery
- **Backend/Frameworks:** FastAPI, Django, Flask, Node.js, Express, Spring Boot, .NET, GraphQL, REST API
- **Databases:** SQL, MySQL, PostgreSQL, MongoDB, SQLite, Redis, Firebase, DynamoDB, Oracle
- **DevOps/Cloud:** Docker, Kubernetes, AWS, Azure, GCP, CI/CD, Jenkins, Terraform, Linux, Nginx
- **Tools/Practices:** Git, GitHub, Agile, Scrum, Jira, Postman
- **Data/ML:** Machine Learning, Deep Learning, Pandas, NumPy, TensorFlow, PyTorch, Scikit-learn, NLP, Tableau, Power BI
- **CS Fundamentals:** DSA, OOP, System Design, Microservices
- **Mobile:** Android, iOS, Flutter, React Native
- **Testing:** Unit Testing, Selenium, Pytest, JUnit

> **Note:** This platform is optimised for Frontend, Backend, and Fullstack developer hiring. The skill list is curated for software/tech roles.

---

## Running Locally

**Prerequisites:** Python 3.10+, pip

```bash
# 1. Clone the repo
git clone https://github.com/Riya-Raj-android/AI_recruitment_platform_with_gemini_ai_features.git
cd AI_recruitment_platform_with_gemini_ai_features

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key
# Create a .env file in the root folder:
echo "GEMINI_API_KEY=your_key_here" > .env
# Get a free key at: https://aistudio.google.com/apikey

# 5. Initialise the database
python -m database.init_db

# 6. Start the backend
python -m uvicorn backend.main:app --reload --port 8000

# 7. Serve the frontend (in a second terminal)
cd frontend
python -m http.server 8080
```

Open `http://127.0.0.1:8080/landing.html` in your browser.

> **Note:** The Gemini API key is only required for AI features (Resume Feedback, Interview Questions, Skill Gap Analysis). All other features (upload, ATS scoring, job matching, ranking) work without it.

---

## Deployment

| Service | Role | URL |
|---------|------|-----|
| **Render** | Backend (FastAPI) | https://ai-recruitment-platform-with-gemini-ai.onrender.com |
| **Netlify** | Frontend (static) | https://sparkling-pony-78afd8.netlify.app |

**Important:** Render's free tier spins down after 15 minutes of inactivity. The first request after a period of inactivity may take 30–60 seconds to respond while the server wakes up. Subsequent requests are fast.

**Environment variable on Render:** Add `GEMINI_API_KEY` in the Render dashboard's Environment tab — never commit it to GitHub.

---

## Known Limitations

- **SQLite on Render free tier:** The database resets on every Render redeploy since free instances use ephemeral disk storage. This is acceptable for a portfolio demo; for production, switch to a hosted PostgreSQL instance (Render offers one free).
- **Gemini free-tier rate limits:** The free Gemini API tier has per-minute and daily request caps. If AI features return a rate-limit message, wait a few minutes and retry. All non-AI features continue to work normally regardless.
- **PDF text extraction:** Works best on digitally generated PDFs (Word → PDF). Scanned/image-based PDFs may yield poor skill detection since `pdfplumber` cannot OCR images.
- **Skill scope:** Currently scoped to tech/software engineering roles. Marketing, finance, HR, or other non-tech job roles will not have their domain-specific skills recognised.

---

## Author

**Riya Raj**  
B.Tech CSE (Data Science Specialisation)  
GitHub: [Riya-Raj-android](https://github.com/Riya-Raj-android)

---

## License

This project is open source and available under the [MIT License](LICENSE).

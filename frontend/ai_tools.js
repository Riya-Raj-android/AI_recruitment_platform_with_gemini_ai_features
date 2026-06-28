const API_BASE = "https://ai-recruitment-platform-with-gemini-ai.onrender.com";

async function loadCandidateOptions() {
    const select = document.getElementById("candidateSelect");

    try {
        const response = await fetch(`${API_BASE}/candidates`);
        const candidates = await response.json();

        if (!candidates.length) {
            select.innerHTML = `<option value="">No candidates uploaded yet</option>`;
            return;
        }

        select.innerHTML = candidates
            .map(c => `<option value="${c.filename}">${c.filename}</option>`)
            .join("");

    } catch (error) {
        select.innerHTML = `<option value="">Failed to load candidates</option>`;
        console.error("ERROR loading candidates:", error);
    }
}

function getSelectedFilename() {
    const select = document.getElementById("candidateSelect");
    const filename = select.value;

    if (!filename) {
        alert("Please select a candidate first.");
        return null;
    }

    return filename;
}

function getJobDescription() {
    return document.getElementById("jobDescription").value.trim();
}

function renderTextResult(targetId, text) {
    const el = document.getElementById(targetId);
    el.className = "result-box";
    el.textContent = text;
}

function setLoading(targetId, label) {
    const el = document.getElementById(targetId);
    el.className = "spinner-text";
    el.textContent = `Generating ${label} with Gemini...`;
}

async function runResumeFeedback() {
    const filename = getSelectedFilename();
    if (!filename) return;

    setLoading("feedbackResult", "resume feedback");

    try {
        const response = await fetch(`${API_BASE}/resume-feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                filename: filename,
                job_description: getJobDescription()
            })
        });

        const data = await response.json();

        if (data.error) {
            renderTextResult("feedbackResult", "Error: " + data.error);
            return;
        }

        renderTextResult("feedbackResult", data.feedback);

    } catch (error) {
        console.error("ERROR:", error);
        renderTextResult("feedbackResult", "Failed: " + error.toString());
    }
}

async function runInterviewQuestions() {
    const filename = getSelectedFilename();
    if (!filename) return;

    setLoading("questionsResult", "interview questions");

    try {
        const response = await fetch(`${API_BASE}/generate-interview-questions`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                filename: filename,
                job_description: getJobDescription()
            })
        });

        const data = await response.json();

        if (data.error) {
            renderTextResult("questionsResult", "Error: " + data.error);
            return;
        }

        renderTextResult("questionsResult", data.questions);

    } catch (error) {
        console.error("ERROR:", error);
        renderTextResult("questionsResult", "Failed: " + error.toString());
    }
}

async function runSkillGap() {
    const filename = getSelectedFilename();
    if (!filename) return;

    setLoading("skillGapResult", "skill gap analysis");

    try {
        const response = await fetch(`${API_BASE}/skill-gap-ai`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                filename: filename,
                job_description: getJobDescription()
            })
        });

        const data = await response.json();

        if (data.error) {
            renderTextResult("skillGapResult", "Error: " + data.error);
            return;
        }

        renderTextResult("skillGapResult", data.analysis);

    } catch (error) {
        console.error("ERROR:", error);
        renderTextResult("skillGapResult", "Failed: " + error.toString());
    }
}

const API_BASE = "https://ai-recruitment-platform-with-gemini-ai.onrender.com";

function scoreBadge(score) {
    let cls = "low";
    if (score >= 70) cls = "high";
    else if (score >= 40) cls = "mid";
    return `<span class="badge ${cls}">${score}%</span>`;
}

function renderMatchResults(data) {
    let header = `<p><strong>Required skills detected:</strong> ${
        data.required_skills.length ? data.required_skills.join(", ") : "(none detected)"
    }</p>`;

    if (!data.candidates.length) {
        return header + "<p class='placeholder'>No candidates uploaded yet.</p>";
    }

    let rows = data.candidates.map(c => `
        <tr>
            <td>${c.filename}</td>
            <td>${scoreBadge(c.ats_score)}</td>
            <td>${c.matched_skills.join(", ") || "-"}</td>
            <td>${c.missing_skills.join(", ") || "-"}</td>
        </tr>
    `).join("");

    return header + `
        <table>
            <thead>
                <tr><th>Filename</th><th>Match</th><th>Matched Skills</th><th>Missing Skills</th></tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>
    `;
}

async function matchJob() {
    const resultDiv = document.getElementById("result");
    const jobDescription = document.getElementById("jobDescription").value.trim();

    if (!jobDescription) {
        alert("Please paste a job description first.");
        return;
    }

    resultDiv.className = "spinner-text";
    resultDiv.textContent = "Matching candidates...";

    try {
        const response = await fetch(`${API_BASE}/match-job`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job_description: jobDescription })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();
        resultDiv.className = "";
        resultDiv.innerHTML = renderMatchResults(data);

    } catch (error) {
        console.error("ERROR:", error);
        resultDiv.className = "placeholder";
        resultDiv.textContent = "Failed to match job: " + error.toString();
    }
}

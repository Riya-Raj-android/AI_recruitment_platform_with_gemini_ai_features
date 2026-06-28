const API_BASE = "http://127.0.0.1:8000";

function scoreBadge(score) {
    let cls = "low";
    if (score >= 70) cls = "high";
    else if (score >= 40) cls = "mid";
    return `<span class="badge ${cls}">${score}%</span>`;
}

function renderRankingTable(candidates) {
    if (!candidates.length) {
        return "<p class='placeholder'>No candidates uploaded yet.</p>";
    }

    let rows = candidates.map((c, index) => `
        <tr>
            <td>#${index + 1}</td>
            <td>${c.filename}</td>
            <td>${c.skills}</td>
            <td>${scoreBadge(c.ats_score)}</td>
        </tr>
    `).join("");

    return `
        <table>
            <thead>
                <tr><th>Rank</th><th>Filename</th><th>Skills</th><th>ATS Score</th></tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>
    `;
}

async function loadRanking() {
    const resultDiv = document.getElementById("result");
    resultDiv.className = "spinner-text";
    resultDiv.textContent = "Loading...";

    try {
        const response = await fetch(`${API_BASE}/ranked-candidates`);

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const candidates = await response.json();
        resultDiv.className = "";
        resultDiv.innerHTML = renderRankingTable(candidates);

    } catch (error) {
        console.error("ERROR:", error);
        resultDiv.className = "placeholder";
        resultDiv.textContent = "Failed to load ranking: " + error.toString();
    }
}

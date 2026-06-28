
const API_BASE = "https://ai-recruitment-platform-with-gemini-ai.onrender.com";

function renderUploadResult(data) {
    if (data.error) {
        return `<p style="color:#dc2626;">${data.error}</p>`;
    }

    if (data.message === "Resume already uploaded") {
        return `<p><strong>${data.filename}</strong> was already uploaded previously.</p>`;
    }

    const skillBadges = (data.skills || [])
        .map(s => `<span class="badge mid" style="margin:3px;">${s}</span>`)
        .join("");

    return `
        <p><strong>${data.filename}</strong> uploaded successfully.</p>
        <p style="margin-bottom:6px;"><strong>Detected skills:</strong></p>
        <div>${skillBadges || "<span class='placeholder'>No recognizable skills found</span>"}</div>
    `;
}

async function uploadResume() {
    const fileInput = document.getElementById("resumeFile");
    const output = document.getElementById("output");

    if (!fileInput.files.length) {
        alert("Please select a PDF file");
        return;
    }

    output.className = "spinner-text";
    output.textContent = "Uploading and analyzing resume...";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch(`${API_BASE}/upload-resume`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();

        output.className = "result-box";
        output.innerHTML = renderUploadResult(data);

    } catch (error) {
        console.error("ERROR:", error);
        output.className = "result-box";
        output.textContent = "Upload failed: " + error.toString();
    }
}
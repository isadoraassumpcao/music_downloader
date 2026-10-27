const button = document.getElementById("downloadButton");
const input = document.getElementById("songInput");
const status = document.getElementById("status");

function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

button.onclick = async () => {
    const rawInput = input.value;
    const songs = rawInput
        .split("\n")
        .map(song => song.trim())
        .filter(song => song !== "");

    if (songs.length === 0) {
        status.innerText = "Please enter at least one song name.";
        return;
    }

    status.innerText = "Adding song(s) to queue...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/download-all",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ songs })
            }
        );

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();
        status.innerText = data.message || `Added ${songs.length} song(s) to the queue.`;
        input.value = "";
        loadQueue();
    } catch (error) {
        status.innerText = "Error: Could not connect to the backend server. Is it running?";
        console.error("Download error:", error);
    }
};

async function loadQueue() {
    try {
        const response = await fetch("http://127.0.0.1:8000/queue");
        if (!response.ok) return;

        const queue = await response.json();
        const container = document.getElementById("queue");

        if (queue.length === 0) {
            container.innerHTML = `<p style="color: #888; font-size: 14px; text-align: center; margin-top: 10px;">Queue is empty.</p>`;
            return;
        }

        container.innerHTML = queue.map(song => {
            const titleDisplay = song.title ? song.title : song.name;
            const subtitleDisplay = (song.title && song.name !== song.title) ? `<div style="font-size: 12px; color: #777; margin-top: 2px;">Query: ${escapeHtml(song.name)}</div>` : "";
            const errorDisplay = (song.status === "failed" && song.error) ? `<div style="font-size: 12px; color: #d63031; margin-top: 4px; word-break: break-word;">${escapeHtml(song.error)}</div>` : "";

            return `
                <div class="queue-item">
                    <div style="flex: 1; padding-right: 15px;">
                        <div class="queue-title">${escapeHtml(titleDisplay)}</div>
                        ${subtitleDisplay}
                        ${errorDisplay}
                    </div>
                    <div class="queue-status">
                        ${getStatus(song.status)}
                    </div>
                </div>
            `;
        }).join("");
    } catch (err) {
        // Backend not yet reachable
    }
}

setInterval(loadQueue, 1000);
loadQueue();

function getStatus(status) {
    switch (status) {
        case "waiting":
            return "⏳ Waiting";
        case "searching":
            return "🔍 Searching";
        case "downloading":
            return "⬇ Downloading";
        case "finished":
            return "✅ Finished";
        case "failed":
            return "❌ Failed";
        default:
            return status;
    }
}

document.getElementById("clearButton").addEventListener("click", clearQueue);

async function clearQueue() {
    try {
        const response = await fetch("http://127.0.0.1:8000/queue/clear", {
            method: "POST"
        });

        const result = await response.json();
        if (result.success) {
            status.innerText = "Queue cleared.";
            loadQueue();
        }
    } catch (error) {
        console.error("Failed to clear queue:", error);
    }
}
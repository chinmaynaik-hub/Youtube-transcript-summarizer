// popup.js

document.addEventListener("DOMContentLoaded", () => {
    const summarizeBtn = document.getElementById("summarize-btn");
    const copyBtn = document.getElementById("copy-btn");
    const loadingEl = document.getElementById("loading");
    const resultEl = document.getElementById("result");
    const errorEl = document.getElementById("error");
    const summaryEl = document.getElementById("summary");

    // Load previously saved optional API key
    const customApiKeyInput = document.getElementById("custom-api-key");
    browser.storage.local.get(['saved_gemini_key']).then(result => {
        if (result.saved_gemini_key) {
            customApiKeyInput.value = result.saved_gemini_key;
        }
    }).catch(err => console.error(err));

    summarizeBtn.addEventListener("click", async () => {
        // Reset state
        resultEl.style.display = "none";
        errorEl.style.display = "none";
        loadingEl.style.display = "flex";
        summarizeBtn.disabled = true;
        summarizeBtn.style.opacity = "0.7";

        // Save API key if entered
        const apiKey = customApiKeyInput.value.trim();
        browser.storage.local.set({ saved_gemini_key: apiKey });

        try {
            // Get the current active tab's URL
            const tabs = await browser.tabs.query({ active: true, currentWindow: true });
            const currentTab = tabs[0];
            const youtubeUrl = currentTab.url;

            // Simple validation to ensure we are on YouTube
            if (!youtubeUrl || !youtubeUrl.includes("youtube.com/watch")) {
                throw new Error("Please open a YouTube video page to summarize.");
            }

            const language = document.getElementById("language-select").value;

            // Call localhost API directly
            const response = await fetch("https://yt-summarizer-in-regional-languages.onrender.com/process_video", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    youtube_link: youtubeUrl,
                    language: language,
                    api_key: apiKey || undefined
                })
            });

            const result = await response.json();

            if (response.ok) {
                // Parse markdown into HTML using marked.js (DOMPurify would be ideal for production)
                const parsedHTML = marked.parse(result.summary);
                // Clear existing content first
                summaryEl.textContent = '';
                // Create a temporary container to parse HTML safely
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = parsedHTML;
                // Append the parsed content
                summaryEl.appendChild(tempDiv);
                // Store raw format for clipboard copying
                summaryEl.dataset.rawMarkdown = result.summary;
                resultEl.style.display = "block";
            } else {
                throw new Error(result.error || "An error occurred while processing the video.");
            }

        } catch (err) {
            errorEl.textContent = err.message || "Network error. Make sure your local Flask backend is running on port 5000.";
            errorEl.style.display = "block";
        } finally {
            loadingEl.style.display = "none";
            summarizeBtn.disabled = false;
            summarizeBtn.style.opacity = "1";
        }
    });

    copyBtn.addEventListener("click", () => {
        const summaryText = summaryEl.dataset.rawMarkdown || summaryEl.innerText;
        navigator.clipboard.writeText(summaryText).then(() => {
            const originalText = copyBtn.innerText;
            copyBtn.innerText = "Copied!";
            setTimeout(() => { copyBtn.innerText = originalText; }, 2000);
        }).catch(err => {
            console.error("Failed to copy text: ", err);
        });
    });
});

function toggleLoader(show) {
    document.getElementById("loader").classList.toggle("hidden", !show);
}

function showToast(message, duration = 3000) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.classList.remove("hidden");
    setTimeout(() => {
        toast.classList.add("hidden");
    }, duration);
}

function disableButtons(disabled) {
    document.querySelectorAll("button").forEach(btn => btn.disabled = disabled);
}

function generateStory() {
    const dream = document.getElementById("dreamInput").value.trim();
    const storyText = document.getElementById("storyText");
    const dreamImage = document.getElementById("dreamImage");
    const themeText = document.getElementById("detectedTheme");
    const emotionText = document.getElementById("detectedEmotion");

    if (!dream) {
        showToast("Please enter your dream first!");
        return;
    }

    toggleLoader(true);
    disableButtons(true);
    storyText.innerText = "Generating your story...";
    themeText.innerText = "...";
    emotionText.innerText = "...";
    dreamImage.src = "";

    fetch("/generate_story", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dream })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) throw new Error(data.error);

        storyText.innerText = data.story;
        dreamImage.src = data.image_url;
        themeText.innerText = data.theme;
        emotionText.innerText = data.emotion;
        showToast("Story generated successfully!");
    })
    .catch(err => {
        storyText.innerText = "Oops! Something went wrong.";
        console.error("Story Error:", err.message);
        showToast("Failed to generate story.");
    })
    .finally(() => {
        toggleLoader(false);
        disableButtons(false);
    });
}

function analyzeDream() {
    const dream = document.getElementById("dreamInput").value.trim();
    const analysisText = document.getElementById("dreamAnalysis");

    if (!dream) {
        showToast("Please enter your dream first!");
        return;
    }

    toggleLoader(true);
    disableButtons(true);
    analysisText.innerText = "Analyzing dream...";

    fetch("/analyze_dream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dream })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) throw new Error(data.error);
        analysisText.innerText = data.analysis;
        showToast("Dream analyzed!");
    })
    .catch(err => {
        analysisText.innerText = "Error analyzing dream.";
        console.error("Analysis Error:", err.message);
        showToast("Failed to analyze dream.");
    })
    .finally(() => {
        toggleLoader(false);
        disableButtons(false);
    });
}
async function analyze() {
    const company = document.getElementById("companyInput").value.trim().toUpperCase();
    const resultCard = document.getElementById("result");
    const placeholder = document.getElementById("placeholder-text");
    const loader = document.getElementById("loader");
    const metricsCard = document.getElementById("metrics-card");

    if (!company) return alert("Enter ticker");

    // UI State: Loading
    placeholder.classList.add("hidden");
    resultCard.classList.add("hidden");
    metricsCard.classList.add("hidden");
    loader.classList.remove("hidden");

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ company })
        });
        const data = await response.json();

        // 1. Set Metrics
        document.getElementById("metrics-grid").innerHTML = `
            <div class="metric-item">Avg Return: <div class="metric-value">${data.metrics.avg_return}</div></div>
            <div class="metric-item">Volatility: <div class="metric-value">${data.metrics.volatility}</div></div>
            <div class="metric-item">Total Return: <div class="metric-value">${data.metrics.total_return}</div></div>
        `;

        // 2. Set Decision
        const badge = document.getElementById("decision-badge");
        badge.innerText = data.decision.toUpperCase();
        badge.className = data.decision.toLowerCase() === 'buy' ? 'buy-bg' : 'sell-bg';

        // 3. Set Explanation
        document.getElementById("explanation-text").innerHTML = `<p>${data.explanation}</p>`;

        // UI State: Success
        loader.classList.add("hidden");
        resultCard.classList.remove("hidden");
        metricsCard.classList.remove("hidden");

    } catch (e) {
        loader.classList.add("hidden");
        placeholder.classList.remove("hidden");
        alert("Server error. Check if backend is running.");
    }
}
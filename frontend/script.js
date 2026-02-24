/**
 * FinRobot JavaScript Controller
 * Handles frontend-to-backend communication and UI state
 */

async function analyze() {
    const companyInput = document.getElementById("companyInput");
    const company = companyInput.value.trim().toUpperCase();
    
    // UI Elements
    const resultCard = document.getElementById("result");
    const placeholder = document.getElementById("placeholder-text");
    const loader = document.getElementById("loader");
    const metricsCard = document.getElementById("metrics-card");
    const metricsGrid = document.getElementById("metrics-grid");
    const badge = document.getElementById("decision-badge");
    const reportTitle = document.getElementById("report-title");
    const explanationText = document.getElementById("explanation-text");

    // Validation
    if (!company) {
        alert("Please enter a stock ticker (e.g., AAPL or TCS.NS)");
        return;
    }

    // 1. UI State: Loading
    placeholder.classList.add("hidden");
    resultCard.classList.add("hidden");
    metricsCard.classList.add("hidden");
    loader.classList.remove("hidden");

    try {
        // 2. API Request
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ company: company }), 
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Backend server error");
        }

        const data = await response.json();

        // 3. Update Performance Metrics
        // We use .toFixed() to keep the UI clean and multiply by 100 for percentages
        metricsGrid.innerHTML = `
            <div class="metric-item">
                Avg Daily Return 
                <div class="metric-value">${(data.metrics.avg_return * 100).toFixed(4)}%</div>
            </div>
            <div class="metric-item">
                Annual Volatility 
                <div class="metric-value">${data.metrics.volatility.toFixed(4)}</div>
            </div>
            <div class="metric-item">
                1Y Total Return 
                <div class="metric-value">${(data.metrics.total_return * 100).toFixed(2)}%</div>
            </div>
        `;

        // 4. Update Decision Badge & Styling
        badge.innerText = data.decision.toUpperCase();
        badge.className = ""; // Reset previous classes
        
        if (data.decision === "INVEST") {
            badge.classList.add("buy-bg");
        } else if (data.decision === "AVOID") {
            badge.classList.add("sell-bg");
        } else {
            // "HOLD" logic - using a custom style for yellow/warning
            badge.style.backgroundColor = "#fbbf24"; 
            badge.style.color = "#000";
        }

        // 5. Update Report Title and AI Explanation
        reportTitle.innerText = `Investment Report: ${data.metrics.symbol}`;
        explanationText.innerHTML = `
            <div style="margin-bottom: 15px; font-weight: bold; color: var(--accent);">
                Source: Live Market Data (FinRobot Online Engine)
            </div>
            <p>${data.explanation}</p>
        `;

        // 6. UI State: Success
        loader.classList.add("hidden");
        resultCard.classList.remove("hidden");
        metricsCard.classList.remove("hidden");

    } catch (e) {
        // 7. Error Handling
        console.error("FinRobot Error:", e);
        loader.classList.add("hidden");
        placeholder.classList.remove("hidden");
        
        alert(`Analysis Failed: ${e.message}. Ensure the backend is running at http://127.0.0.1:8000`);
    }
}

// Allow pressing "Enter" key to trigger analysis
document.getElementById("companyInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        analyze();
    }
});
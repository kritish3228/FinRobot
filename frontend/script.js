async function analyze() {
    const company = document.getElementById("companyInput").value.trim();
    const resultDiv = document.getElementById("result");

    if (!company) {
        resultDiv.innerText = "Please enter a company symbol.";
        return;
    }

    resultDiv.innerText = "Analyzing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ company })
        });

        const data = await response.json();

        resultDiv.innerText =
            `Decision: ${data.decision}\n\n` +
            `Average Return: ${data.metrics.avg_return}\n` +
            `Volatility: ${data.metrics.volatility}\n` +
            `Total Return: ${data.metrics.total_return}\n\n` +
            `Explanation:\n${data.explanation}`;

    } catch (error) {
        resultDiv.innerText = "Error connecting to backend.";
    }
}

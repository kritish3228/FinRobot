from fastapi import FastAPI
from pydantic import BaseModel

from backend.finrobot_service import analyze_company
from backend.llm_agent import explain

app = FastAPI(title="FinRobot Backend")

class AnalyzeRequest(BaseModel):
    company: str

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    metrics = analyze_company(req.company)

    try:
        explanation = explain(metrics)
    except Exception:
        explanation = "LLM explanation unavailable."

    return {
        "decision": metrics["decision"],
        "metrics": metrics,
        "explanation": explanation
    }

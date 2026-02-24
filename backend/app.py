import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import your internal logic
# Ensure these files exist in your 'backend' folder
from backend.finrobot_service import analyze_company
from backend.llm_agent import explain

app = FastAPI(
    title="FinRobot API",
    description="Backend engine for AI-driven stock analysis",
    version="1.0.0"
)

# --- CORS CONFIGURATION ---
# This allows your frontend (likely on port 5500) to communicate with this API (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class AnalyzeRequest(BaseModel):
    company: str

# --- ROUTES ---

@app.get("/")
def health_check():
    return {"status": "online", "message": "FinRobot Backend is running"}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """
    Takes a ticker symbol, fetches live data, calculates metrics,
    and returns an AI-generated explanation.
    """
    ticker = req.company.strip().upper()
    
    try:
        # 1. Run Financial Analysis
        # This calls your yfinance logic in finrobot_service.py
        metrics = analyze_company(ticker)

        # 2. Generate AI Explanation
        try:
            explanation = explain(metrics)
        except Exception as e:
            print(f"LLM Error: {e}")
            explanation = (
                f"Financial analysis for {ticker} is complete, but the AI summary "
                "is currently unavailable. Please check the metrics dashboard."
            )

        # 3. Return consolidated JSON response
        return {
            "status": "success",
            "decision": metrics["decision"],
            "metrics": metrics,
            "explanation": explanation
        }

    except ValueError as ve:
        # Specifically handles "Ticker Not Found" or data errors
        raise HTTPException(status_code=404, detail=str(ve))
    
    except Exception as e:
        # Handles unexpected system errors
        print(f"System Error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred while processing the market data."
        )

# --- SERVER START ---
if __name__ == "__main__":
    # Start the server on localhost:8000
    # reload=True allows the server to restart automatically when you save code
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
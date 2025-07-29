from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.pipeline import analyze_message

app = FastAPI()

# CORS: Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class MessageRequest(BaseModel):
    text: str

# Response schema
class AnalysisResponse(BaseModel):
    verdict: str
    icon: str
    label: str  # <- This must be a string, not a dict
    confidence: float
    source: str
    reason: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: MessageRequest):
    raw_result = analyze_message(request.text)

    # Ensure formatting
    response = {
        "verdict": raw_result.get("verdict", "Unknown"),
        "icon": raw_result.get("icon", "❓"),
        "label": str(raw_result.get("label", "unknown")),  # force to string
        "confidence": float(raw_result.get("confidence", 0.0)),
        "source": raw_result.get("source", "classifier"),
        "reason": raw_result.get("reason", "No reason provided"),
    }

    return response
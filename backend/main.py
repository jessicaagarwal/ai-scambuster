from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.pipeline import analyze_message

app = FastAPI(
    title="AI ScamBuster",
    description="Real-time AI-powered scam detection and explanation assistant",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define input model for JSON
class MessageInput(BaseModel):
    message: str

# ✅ Update endpoint to accept JSON
@app.post("/analyze")
def analyze(input: MessageInput):
    """
    Analyze a message to detect scam and explain if needed.
    """
    result = analyze_message(input.message)
    return result
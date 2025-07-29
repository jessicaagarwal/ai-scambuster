from backend.model.classifier import classify_message
from backend.ingest.utils import heuristic_override
from backend.rag_chat import explain_scam

def analyze_message(message: str) -> dict:
    """
    Run classification and explanation pipeline on the input message.

    Returns:
        {
            "prediction": {
                "label": "spam" or "not spam",
                "confidence": float
            },
            "explanation": str
        }
    """
    # 1. Classify using HuggingFace spam detection
    prediction = classify_message(message)

    if prediction.get("error"):
        return {"error": prediction["error"]}

    # 2. Generate intelligent explanation if it's spam
    if prediction["label"] == "spam":
        explanation = explain_scam(message)
    else:
        explanation = "✅ This message appears safe. Still, stay cautious with unknown links or requests."

    return {
        "prediction": prediction,
        "explanation": explanation
    }
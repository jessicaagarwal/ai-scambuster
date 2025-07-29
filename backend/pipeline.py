from backend.model.classifier import remote_classify
from backend.rag_chat import explain_scam

def analyze_message(message: str) -> dict:
    # Step 1: Call HuggingFace classifier
    classification = remote_classify(message)

    # Step 2: Parse response
    label = classification.get("label", "unknown")
    confidence = classification.get("confidence", 0.0)
    source = classification.get("source", "unknown")

    # Step 3: Use fallback if model failed badly
    if label == "unknown":
        verdict = "Safe Message"
        icon = "✅"
        reason = "Unable to classify message. Fallback assumed safe."
    elif label == "spam":
        verdict = "Scam Detected"
        icon = "🛡️"
        reason = explain_scam(message)
    else:
        verdict = "Safe Message"
        icon = "✅"
        reason = "No scam indicators found."

    # Step 4: Return structured result
    return {
        "verdict": verdict,
        "icon": icon,
        "label": label,
        "confidence": round(confidence, 2),
        "source": source,
        "reason": reason,
    }
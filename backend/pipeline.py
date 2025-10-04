from backend.model.classifier import remote_classify
from backend.rag_chat import explain_scam

def analyze_message(message: str) -> dict:
    # Step 1: Call HuggingFace classifier
    classification = remote_classify(message)

    # Step 2: Parse response
    label = classification.get("label", "unknown")
    confidence = float(classification.get("confidence", 0.0))

    # Step 3: Map to unified verdicts and sources
    if label == "spam":
        verdict = "SCAM"
        icon = "🚨"
        # When we generate an explanation via RAG, mark source as knowledge-base
        source = "knowledge-base"
        reason = explain_scam(message)
    elif label == "ham":
        verdict = "SAFE"
        icon = "✅"
        source = "classifier"
        reason = "No scam indicators found."
    else:
        # Unknown -> treat as suspicious
        verdict = "SUSPICIOUS"
        icon = "⚠️"
        source = "classifier"
        reason = "Unable to confidently classify the message."

    # Step 4: Return structured result
    return {
        "verdict": verdict,
        "icon": icon,
        "label": label,
        "confidence": round(confidence, 2),
        "source": source,
        "reason": reason,
    }
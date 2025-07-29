import os
import requests
from backend.ingest.utils import heuristic_override
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")

MODEL_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-sms-spam-detection"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def remote_classify(text: str) -> dict:
    try:
        response = requests.post(
            MODEL_URL,
            headers=HEADERS,
            json={"inputs": text},
            timeout=8,
        )
        result = response.json()
        print("[DEBUG] HuggingFace API raw response:", result)

        # Check if we got nested lists
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            predictions = result[0]  # grab the inner list
        else:
            predictions = result

        # Find the label with the highest score
        if isinstance(predictions, list) and predictions:
            top = max(predictions, key=lambda x: x["score"])
            label = "spam" if top["label"] == "LABEL_1" else "ham"
            confidence = top["score"]
        else:
            label = "unknown"
            confidence = 0.0

        # Run heuristic override
        heuristic_label, reason = heuristic_override(text)
        if heuristic_label == "spam" and label != "spam":
            print(f"[OVERRIDE] Heuristic forced 'spam' due to: {reason}")
            return {
                "label": "spam",
                "confidence": 0.75,
                "source": "heuristic + hf",
                "reason": reason,
            }

        return {
            "label": label,
            "confidence": confidence,
            "source": "huggingface",
            "reason": "No scam indicators found." if label == "ham" else "High spam score from model",
        }

    except Exception as e:
        print(f"[ERROR] HF API call failed: {e}")
        return {
            "label": "unknown",
            "confidence": 0.0,
            "source": "heuristic (API error)",
            "reason": "Failed to connect to model",
        }
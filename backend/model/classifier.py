from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

client = InferenceClient(
    model="mrm8488/bert-tiny-finetuned-sms-spam-detection",
    token=HF_API_TOKEN
)

def classify_message(text: str) -> dict:
    """
    Classify message using HuggingFace Inference API and return label + confidence
    """
    try:
        response = client.text_classification(text)
        pred = response[0]
        return {
            "label": "spam" if pred["label"].lower() == "spam" else "not spam",
            "confidence": round(pred["score"], 3)
        }
    except Exception as e:
        return {
            "label": "unknown",
            "confidence": 0.0,
            "error": str(e)
        }
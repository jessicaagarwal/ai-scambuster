# backend/model/classifier.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-sms-spam-detection"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def classify_message(message: str):
    payload = {"inputs": message}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        label = result[0][0]["label"]
        confidence = result[0][0]["score"]
        return {
            "label": "spam" if label == "LABEL_1" else "not spam",
            "confidence": round(confidence * 100, 2)
        }
    except Exception as e:
        return {"error": str(e)}

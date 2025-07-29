def tag_text(text: str) -> list:
    text = text.lower()
    tags = []

    if "win" in text or "prize" in text or "jackpot" in text:
        tags.append("lottery_scam")
    if "job" in text or "offer" in text or "hiring" in text:
        tags.append("job_offer_scam")
    if "bank" in text or "transfer" in text or "account" in text:
        tags.append("advance_fee_fraud")
    if "romance" in text or "love" in text or "dating" in text:
        tags.append("romance_fraud")
    if "click" in text or "link" in text or "login" in text:
        tags.append("phishing")

    return tags or ["general_scam"]

SCAM_KEYWORDS = [
    "lottery", "click here", "claim your prize", "free", "urgent",
    "win", "reward", "gift", "congratulations", "credit card", "money",
    "verify", "limited time", "offer", "act now", "guaranteed"
]

def heuristic_override(text: str) -> tuple[str, str]:
    lower_text = text.lower()
    for keyword in SCAM_KEYWORDS:
        if keyword in lower_text:
            return "spam", f"Keyword match: '{keyword}'"
    return "ham", ""
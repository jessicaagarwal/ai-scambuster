from datasets import load_dataset

def load_sms_spam_dataset():
    dataset = load_dataset("sms_spam", split="train")

    entries = []

    for i, row in enumerate(dataset):
        if i < 5:
            print("[DEBUG] Row:", row)

        label = int(row["label"])  # force cast
        if label == 1:
            entries.append({
                "text": row["sms"],
                "metadata": {
                    "source": "huggingface_sms_spam",
                    "tag": "sms_spam"
                }
            })

    print(f"[DEBUG] Total spam samples loaded: {len(entries)}")
    return entries

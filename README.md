# 🚨 AI ScamBuster

**AI ScamBuster** is a real-time AI-powered cybersecurity assistant that detects, classifies, and explains scam messages using a combination of machine learning and Retrieval-Augmented Generation (RAG). It doesn't just say *"this is spam"* — it tells you **why**.

---

## 🧠 Features

- 🔍 **Real-time Scam Classification** using HuggingFace Inference API.
- 🤖 **Smart Reasoning** powered by Groq's LLaMA3-70B for human-like scam explanation.
- 🔐 **Tag-Based Vector Retrieval** from a FAISS vectorstore built with filtered cybercrime knowledge.
- ⚡ **FastAPI Backend** with modular architecture (ingest, model, vectorstore, pipeline).
- 🖥️ **Cyberpunk-Themed React Frontend** for an immersive user experience.
- 🧪 **Custom Confidence Thresholds** and Multi-Label Classification (`spam`, `suspicious`, `safe`).

---

## 🛠️ Tech Stack

| Area        | Tech                            |
|-------------|---------------------------------|
| Frontend    | React.js, TailwindCSS           |
| Backend     | FastAPI, HuggingFace, Groq      |
| ML/RAG      | LLaMA3-70B, FAISS, LangChain     |
| Embeddings  | Sentence Transformers (MiniLM)  |
| Vectorstore | FAISS                           |
| Hosting     | Local (for now)                 |

---

## 📁 Project Structure

```
ai-scambuster/
├── backend/
│   ├── ingest/            # Dataset loading and tag filtering
│   ├── model/             # Classifier and embedding setup
│   ├── vectorstore/       # FAISS index setup and retrieval
│   ├── pipeline.py        # Classification and reasoning pipeline
│   ├── rag_chat.py        # LLaMA3 response logic
│   └── main.py            # FastAPI server entry
├── frontend/
│   ├── App.jsx            # Cyberpunk UI with API integration
│   └── ...
└── data/                  # PDF and message datasets
```

---

## ⚙️ How to Run

### Backend

```bash
cd backend
python ingest/huggingface_loader.py        # Load and filter spam samples
python vectorstore/index.py                # Build FAISS vectorstore
uvicorn main:app --reload                  # Start FastAPI server
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## ✅ Sample API Usage

**POST** \`/analyze\`

```json
{
  "text": "Congratulations! You have won a free iPhone. Click here to claim your prize now."
}
```

**Response**
```json
{
  "verdict": "Scam",
  "label": "phishing",
  "confidence": 0.91,
  "source": "classifier",
  "reason": "This message promises unrealistic rewards and includes language typical of prize scams. Common in phishing attacks."
}
```

---

## 🔐 Security Focus

- Sensitive info like HuggingFace tokens stored in \`.env\`
- CORS-protected API endpoints
- Plans for user feedback loop and scam pattern analytics

---

## 📌 Future Roadmap

- [ ] Integrate user feedback for RLHF-style learning
- [ ] Browser extension for scam detection on the go
- [ ] Fine-tune classifier on custom scam types (job scams, impersonation)
- [ ] Deploy with Docker & CI/CD

---

> Built by **Jessica Agarwal**  
> [GitHub](https://github.com/jessicaagarwal) | [LinkedIn](https://www.linkedin.com/in/jessica-agarwal-00b6b7225/)

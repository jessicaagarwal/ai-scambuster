from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import os
import pickle
from groq import Groq

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Use the tested working embedder
embedding = HuggingFaceInferenceAPIEmbeddings(
    api_key=HF_TOKEN,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ✅ Load FAISS vectorstore
with open("backend/vectorstore/spam_faiss.pkl", "rb") as f:
    faiss_store = pickle.load(f)

print("✅ Vectorstore loaded. Type your message (e.g., suspicious SMS):\n")

# Initialize Groq client for LLaMA3
groq_client = Groq(api_key=GROQ_API_KEY)

while True:
    query = input("🔍 Your message: ").strip()
    if not query:
        continue

    try:
        docs_and_scores = faiss_store.similarity_search_with_score(query, k=3)
    except Exception as e:
        print(f"[ERROR] Similarity search failed: {e}")
        continue

    context_texts = "\n---\n".join(
        [f"[Similarity Score: {round(score, 4)}]\n{doc.page_content}" for doc, score in docs_and_scores]
    )

    prompt = f"""
You are an SMS spam classification assistant.

Based on the following retrieved messages from a spam corpus, determine if the user query is spam or not. Be direct.

Retrieved Examples:
{context_texts}

User Message:
\"{query}\"

Answer in this format:
Spam Probability: (High | Medium | Low)
Reasoning: <short explanation>
Final Verdict: (Spam | Not Spam)
"""

    try:
        chat_response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        reply = chat_response.choices[0].message.content
        print("\n🤖 LLaMA3 Response:\n", reply)
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}")

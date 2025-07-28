from ingest.huggingface_loader import load_sms_spam_dataset
from ingest.utils import tag_text
from model.embedder import get_embedder
from vectorstore.index import get_vectorstore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv
import os
import pickle

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize embedding model
embedding = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=HF_TOKEN
)

def run_pipeline():
    # Load and prepare data
    data = load_sms_spam_dataset()
    texts = [entry["text"] for entry in data]
    metadatas = [entry["metadata"] for entry in data]

    print(f"[DEBUG] Loaded {len(texts)} texts and {len(metadatas)} metadatas.")

    # Build and save vectorstore
    vs = get_vectorstore(texts=texts, metadatas=metadatas, embedding_function=embedding)
    os.makedirs("vectorstore", exist_ok=True)
    with open("backend/vectorstore/spam_faiss.pkl", "wb") as f:
        pickle.dump(vs, f)
    
    print(f"✅ {len(texts)} spam messages embedded and vectorstore saved.")

if __name__ == "__main__":
    run_pipeline()
import os
import warnings
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq
import logging
import traceback

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
os.environ["NUMEXPR_MAX_THREADS"] = "8"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_embedding_model():
    """Initialize and validate the embedding model."""
    try:
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={
                'device': 'cpu',
                'trust_remote_code': True
            },
            encode_kwargs={
                'normalize_embeddings': True,
                'batch_size': 32
            }
        )
        
        # Validate embeddings
        test_embedding = embedding.embed_query("Test message")
        if not test_embedding or len(test_embedding) != 384:
            raise ValueError(f"Invalid embedding dimension: {len(test_embedding) if test_embedding else 0}")
        
        logger.info("✓ Embedding model initialized successfully")
        return embedding
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize embedding model: {str(e)}")
        raise

def load_vectorstore(embedding):
    """Load and validate the FAISS vectorstore."""
    try:
        vectorstore = FAISS.load_local(
            "backend/vectorstore/faiss_index",
            embedding,
            allow_dangerous_deserialization=True
        )
        logger.info("✓ Vectorstore loaded successfully")
        return vectorstore.as_retriever()
    except Exception as e:
        logger.error(f"❌ Failed to load vectorstore: {str(e)}")
        raise

# Initialize components
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")

if not hf_token or not groq_api_key:
    raise ValueError("Required API tokens not found in environment")

embedding = initialize_embedding_model()
retriever = load_vectorstore(embedding)

# Initialize LLM
llm = ChatGroq(
    model_name="llama3-70b-8192",
    api_key=groq_api_key
)

# RAG-style explanation prompt
template = """
You are an AI cybersecurity expert trained on global scam and fraud data. Your job is to explain why a given message might be a scam, based on the context below.

Context:
{context}

Question: Why is the following message suspicious?
Message: "{message}"

Provide a clear, concise explanation in under 100 words.
"""

prompt = PromptTemplate(
    input_variables=["context", "message"],
    template=template
)

def _fallback_explanation(message: str) -> str:
    """Provide a concise, user-friendly heuristic explanation when RAG fails."""
    text = (message or "").lower()
    indicators = []
    if any(k in text for k in ["bank", "account", "verify", "otp", "password"]):
        indicators.append("requests sensitive banking or login details")
    if any(k in text for k in ["click", "link", "http://", "https://", "login", "verify-account"]):
        indicators.append("contains a link urging immediate action")
    if any(k in text for k in ["urgent", "24 hours", "immediately", "suspend", "closure"]):
        indicators.append("uses urgency or threats to pressure you")
    if any(k in text for k in ["win", "prize", "reward", "free", "jackpot"]):
        indicators.append("promises rewards to lure a response")
    if not indicators:
        indicators.append("matches common scam patterns (urgency, links, or requests for credentials)")
    return (
        "Potential scam indicators: " + "; ".join(indicators) + ". "
        "Never enter credentials from unsolicited messages; verify via official channels."
    )

# Explanation function
def explain_scam(text: str) -> str:
    """Analyze text for potential scam indicators using RAG with graceful fallback."""
    try:
        logger.debug(f"Processing text: {text}")
        
        if not text or not isinstance(text, str):
            raise ValueError("Invalid input text")

        # Get relevant documents
        try:
            docs = retriever.invoke(text)
            if not docs:
                logger.warning("No relevant context found; using fallback explanation")
                return _fallback_explanation(text)
            context = "\n\n".join([doc.page_content for doc in docs])
            logger.debug(f"Retrieved {len(docs)} relevant documents")
        except Exception as e:
            logger.error(f"Retriever error: {str(e)}; using fallback explanation")
            return _fallback_explanation(text)

        # Generate explanation
        try:
            response = llm.invoke(prompt.format(context=context, message=text))
            return response.content if hasattr(response, "content") else str(response)
        except Exception as e:
            logger.error(f"LLM error: {str(e)}; using fallback explanation")
            return _fallback_explanation(text)

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return _fallback_explanation(text)
    except Exception:
        logger.error("Unexpected error:")
        logger.error(traceback.format_exc())
        return _fallback_explanation(text)
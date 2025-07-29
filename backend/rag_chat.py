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

# Explanation function
def explain_scam(text: str) -> str:
    """Analyze text for potential scam indicators using RAG."""
    try:
        logger.debug(f"Processing text: {text}")
        
        if not text or not isinstance(text, str):
            raise ValueError("Invalid input text")

        # Get relevant documents
        try:
            docs = retriever.invoke(text)
            if not docs:
                raise ValueError("No relevant context found")
            context = "\n\n".join([doc.page_content for doc in docs])
            logger.debug(f"Retrieved {len(docs)} relevant documents")
        except Exception as e:
            logger.error(f"Retriever error: {str(e)}")
            return "Error: Unable to retrieve context"

        # Generate explanation
        try:
            response = llm.invoke(prompt.format(context=context, message=text))
            return response.content if hasattr(response, "content") else str(response)
        except Exception as e:
            logger.error(f"LLM error: {str(e)}")
            return "Error: Unable to generate explanation"

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return f"Error: {str(ve)}"
    except Exception as e:
        logger.error("Unexpected error:")
        logger.error(traceback.format_exc())
        return "Unable to analyze due to backend error"
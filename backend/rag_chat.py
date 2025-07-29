import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")

embedding = HuggingFaceInferenceAPIEmbeddings(
    api_key=hf_token,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS index
vectorstore = FAISS.load_local("backend/vectorstore/faiss_index", embedding, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# Prompt template for explanation
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

llm = ChatGroq(
    model_name="llama3-70b-8192",
    api_key=groq_api_key
)

def explain_scam(message: str) -> str:
    """
    Generate scam explanation using RAG over vector DB.
    """
    docs: list[Document] = retriever.get_relevant_documents(message)
    context = "\n".join([doc.page_content for doc in docs[:3]])  # Top 3 relevant chunks

    prompt_text = prompt.format(context=context, message=message)
    response = llm.invoke(prompt_text)

    return response.content
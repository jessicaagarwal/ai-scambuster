from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access token
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HUGGINGFACE_TOKEN:
    raise ValueError("⚠️ HUGGINGFACEHUB_API_TOKEN not found in .env")
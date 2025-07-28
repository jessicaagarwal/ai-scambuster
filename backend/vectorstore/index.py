from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss

def get_vectorstore(texts, metadatas, embedding_function):
    dim = 384  # for sentence-transformers/all-MiniLM-L6-v2
    index = faiss.IndexFlatL2(dim)

    # Now initialize using .from_texts() — this handles everything internally
    return FAISS.from_texts(
        texts=texts,
        embedding=embedding_function,
        metadatas=metadatas
    )
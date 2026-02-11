from __future__ import annotations
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from retrieval.document_loader import load_and_chunk_documents

load_dotenv()

INDEX_DIR = Path("data/index")
FAISS_PATH = INDEX_DIR / "faiss_index"

def build_vector_index() -> FAISS:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    chunks: List[Document] = load_and_chunk_documents()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    vectorstore.save_local(str(FAISS_PATH))

    print(
        f"[VectorStore] Saved FAISS index with {len(chunks)} chunks → {FAISS_PATH}"
    )

    return vectorstore

def load_vector_index() -> FAISS:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return FAISS.load_local(
        str(FAISS_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )

def ensure_vector_index() -> FAISS:
    index_file = FAISS_PATH / "index.faiss"

    if index_file.exists():
        print("[VectorStore] Loading existing FAISS index")
        return load_vector_index()

    print("[VectorStore] No valid index found, building a new one")
    return build_vector_index()

if __name__ == "__main__":
    ensure_vector_index()

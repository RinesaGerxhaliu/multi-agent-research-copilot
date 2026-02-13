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
EMBEDDING_MODEL = "text-embedding-3-small"

def is_valid_index(path: Path) -> bool:
    return (path / "index.faiss").exists() and (path / "index.pkl").exists()

def build_vector_index() -> FAISS:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    chunks: List[Document] = load_and_chunk_documents()

    if not chunks:
        raise ValueError("[VectorStore] No chunks found. Cannot build index.")

    print(f"[VectorStore] Using embedding model: {EMBEDDING_MODEL}")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    vectorstore.save_local(str(FAISS_PATH))

    print(f"[VectorStore] Saved FAISS index with {len(chunks)} chunks")
    print(f"[VectorStore] Index path: {FAISS_PATH.resolve()}")

    return vectorstore

def load_vector_index() -> FAISS:
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    print("[VectorStore] Loading existing FAISS index")

    return FAISS.load_local(
        str(FAISS_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )

def ensure_vector_index() -> FAISS:
    if is_valid_index(FAISS_PATH):
        return load_vector_index()

    print("[VectorStore] No valid index found, building new one")
    return build_vector_index()

if __name__ == "__main__":
    ensure_vector_index()

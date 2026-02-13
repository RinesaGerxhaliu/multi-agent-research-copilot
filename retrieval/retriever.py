from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

VECTORSTORE_PATH = Path("data/index/faiss_index")
EMBEDDING_MODEL = "text-embedding-3-small"

class Retriever:

    def __init__(self):

        if not VECTORSTORE_PATH.exists():
            raise FileNotFoundError(
                "[Retriever] FAISS index not found. Run vector index build first."
            )

        print(f"[Retriever] Using embedding model: {EMBEDDING_MODEL}")

        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

        self.vectorstore = FAISS.load_local(
            str(VECTORSTORE_PATH),
            embeddings,
            allow_dangerous_deserialization=True,
        )

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:

        if not query.strip():
            return []

        k = max(1, min(k, 10))

        results = self.vectorstore.similarity_search_with_score(query, k=k)

        results = sorted(results, key=lambda x: x[1])

        formatted = []

        for rank, (doc, score) in enumerate(results, start=1):

            snippet = doc.page_content[:400].replace("\n", " ").strip()

            formatted.append({
                "rank": rank,
                "snippet": snippet,
                "document_name": doc.metadata.get("document_name"),
                "chunk_id": doc.metadata.get("chunk_id"),
                "citation": doc.metadata.get("citation"),
                "source_id": doc.metadata.get("source_id"),
                "start_index": doc.metadata.get("start_index"),
                "distance_score": float(score),
            })

        print(f"[Retriever] Retrieved {len(formatted)} results for query.")
        return formatted

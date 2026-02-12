from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

VECTORSTORE_PATH = Path("data/index/faiss_index")

class Retriever:

    def __init__(self):

        if not VECTORSTORE_PATH.exists():
            raise FileNotFoundError(
                "FAISS index not found. Run vector index build first."
            )

        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        self.vectorstore = FAISS.load_local(
            str(VECTORSTORE_PATH),
            embeddings,
            allow_dangerous_deserialization=True
        )

    def search(self, query: str, k: int = 5):

        results = self.vectorstore.similarity_search_with_score(query, k=k)

        formatted = []

        for doc, score in results:
            formatted.append({
                "content": doc.page_content,
                "document_name": doc.metadata.get("document_name"),
                "chunk_id": doc.metadata.get("chunk_id"),
                "source_id": doc.metadata.get("source_id"),
                "distance_score": float(score)  
            })

        return formatted

from __future__ import annotations
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = Path("data/sample_docs")

SUPPORTED_EXTS = {".md", ".txt"}

def load_raw_documents() -> List[Document]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data path not found: {DATA_PATH}")

    documents: List[Document] = []

    for path in DATA_PATH.iterdir():
        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTS:
            continue

        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "document_name": path.name,
                    "source_path": str(path).replace("\\", "/"),
                    "file_ext": path.suffix.lower(),
                },
            )
        )

    return documents

def chunk_documents(
    documents: List[Document],
    chunk_size: int = 600,
    chunk_overlap: int = 100,
) -> List[Document]:
 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )

    chunks: List[Document] = []

    for doc in documents:
        splits = splitter.split_documents([doc])

        for i, chunk in enumerate(splits):
            chunk.metadata = dict(chunk.metadata)

            chunk.metadata["chunk_id"] = i
            chunk.metadata["source_id"] = (
                f"doc:{chunk.metadata.get('document_name')}#chunk_{i}"
            )

            chunks.append(chunk)

    return chunks

def load_and_chunk_documents() -> List[Document]:
    raw_docs = load_raw_documents()
    chunks = chunk_documents(raw_docs)

    print(f"[Loader] Loaded {len(raw_docs)} docs → {len(chunks)} chunks")
    return chunks

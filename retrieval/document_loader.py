from __future__ import annotations
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = Path("data/sample_docs")
SUPPORTED_EXTS = {".md", ".txt"}

def load_raw_documents() -> List[Document]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"[Loader] Data path not found: {DATA_PATH}")

    documents: List[Document] = []

    for path in sorted(DATA_PATH.iterdir()):
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
                    "document_id": path.stem,
                    "source_path": str(path).replace("\\", "/"),
                    "file_ext": path.suffix.lower(),
                },
            )
        )

    print(f"[Loader] Loaded {len(documents)} raw documents")
    return documents

def chunk_documents(
    documents: List[Document],
    chunk_size: int = 700,
    chunk_overlap: int = 120,
) -> List[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )

    chunks: List[Document] = []
    global_chunk_id = 0

    for doc in documents:
        splits = splitter.split_documents([doc])

        for chunk in splits:
            chunk.metadata = dict(chunk.metadata)

            chunk.metadata["chunk_id"] = global_chunk_id

            chunk.metadata["citation"] = (
                f"{chunk.metadata.get('document_name')}#chunk_{global_chunk_id}"
            )

            chunk.metadata["source_id"] = (
                f"doc:{chunk.metadata.get('document_name')}#chunk_{global_chunk_id}"
            )

            chunks.append(chunk)
            global_chunk_id += 1

    print(f"[Loader] Created {len(chunks)} total chunks")
    return chunks

def load_and_chunk_documents() -> List[Document]:
    raw_docs = load_raw_documents()
    chunks = chunk_documents(raw_docs)

    print(f"[Loader] {len(raw_docs)} docs → {len(chunks)} chunks ready")
    return chunks


if __name__ == "__main__":
    load_and_chunk_documents()

"""Build the Alloba FAISS knowledge index from kb/docs.

Usage:
    python ingest.py

Requires a running Ollama server (``ollama serve``) with the embedding model
configured via ALLOBA_EMBEDDING_MODEL (default ``nomic-embed-text``).
The index is written with safe serialization (binary + JSON, no pickle).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from langchain_ollama import OllamaEmbeddings

from alloba.config import settings
from alloba.ingestion import DocumentIngestionService


def main() -> None:
    embeddings = OllamaEmbeddings(model=settings.embedding_model, base_url=settings.ollama_base_url)
    service = DocumentIngestionService(
        embedding_model=embeddings,
        docs_dir=settings.rag_docs_dir,
        index_dir=settings.rag_index_dir,
    )
    result = service.build()
    print(
        f"Indexed {result['documents']} documents into {result['chunks']} chunks "
        f"at {result['index_dir']}"
    )


if __name__ == "__main__":
    main()

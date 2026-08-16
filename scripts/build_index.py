"""Build the Alloba FAISS knowledge index from kb/docs (thin wrapper).

Usage:
    python scripts/build_index.py

Equivalent to `python ingest.py` at the repository root. Requires a running
Ollama server. The index is written with safe serialization only.
"""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src"))

from langchain_ollama import OllamaEmbeddings  # noqa: E402

from alloba.config import settings  # noqa: E402
from alloba.ingestion import DocumentIngestionService  # noqa: E402


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

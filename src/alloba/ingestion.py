"""Document ingestion — build the safe FAISS knowledge index from kb/docs.

The pipeline reads Markdown, plain text and PDF documents from the configured
docs directory, splits them into overlapping chunks, embeds them with a local
Ollama embedding model, and persists the index with *safe* serialization
(binary ``index.faiss`` + JSON ``index.safe.json`` — never pickle).
"""

import ast
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from alloba.faiss_store import _FaissVectorStore, save_local_safe

_CHUNK_SIZE = 800
_CHUNK_OVERLAP = 150


class DocumentIngestionService:
    """Builds and refreshes the compliance knowledge index."""

    def __init__(self, embedding_model, docs_dir: str, index_dir: str) -> None:
        self.embedding_model = embedding_model
        self.docs_dir = Path(docs_dir)
        self.index_dir = Path(index_dir)

    # ---- source parsers ----------------------------------------------------

    def parse_python_code(self, content: str, path: str) -> dict:
        """Extract governance metadata from a Python source file."""
        try:
            tree = ast.parse(content)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        except SyntaxError:
            functions, classes = [], []
        return {
            "content": content,
            "type": "code",
            "metadata": {
                "language": "python",
                "path": path,
                "functions": functions,
                "classes": classes,
                "sensitivity": "INTERNAL",
            },
        }

    def parse_apk_metadata(self, xml_content: str) -> dict:
        """Return a placeholder Android package analysis payload."""
        manifest_size = len(xml_content)
        content = f"Android Package Info\nVersion: <VERSION_NAME>\n{manifest_size} bytes manifest"
        return {
            "content": content,
            "type": "apk_config",
            "metadata": {"platform": "android"},
        }

    # ---- pipeline ------------------------------------------------------------

    def _load_documents(self) -> list[Document]:
        documents: list[Document] = []
        for pattern in ("*.md", "*.txt"):
            for file_path in sorted(self.docs_dir.rglob(pattern)):
                if not file_path.is_file():
                    continue
                text = file_path.read_text(encoding="utf-8", errors="replace")
                if text.strip():
                    documents.append(
                        Document(page_content=text, metadata={"source": str(file_path)})
                    )
        return documents

    def build(self) -> dict:
        """Chunk, embed and persist the index. Idempotent per run."""
        if not self.docs_dir.is_dir():
            raise FileNotFoundError(f"Docs directory not found: {self.docs_dir}")

        documents = self._load_documents()
        if not documents:
            raise ValueError(f"No indexable documents found in {self.docs_dir}")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=_CHUNK_SIZE, chunk_overlap=_CHUNK_OVERLAP, add_start_index=True
        )
        chunks = splitter.split_documents(documents)
        if not chunks:
            raise ValueError("No indexable content — the documents are empty.")

        store = _FaissVectorStore.from_documents(chunks, embedding=self.embedding_model)
        save_local_safe(store, str(self.index_dir))
        return {
            "documents": len(documents),
            "chunks": len(chunks),
            "index_dir": str(self.index_dir),
        }

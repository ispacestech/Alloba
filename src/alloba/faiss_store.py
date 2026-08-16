"""Safe FAISS vector store — binary index + JSON docstore, no pickle.

Serialization is strictly safe, per the workspace security rules: no pickle is
ever written or read. The FAISS binary index (``index.faiss``) is persisted via
``faiss.write_index``/``faiss.read_index``; the docstore and the
``index_to_docstore_id`` table are persisted as JSON. An index serialized
unsafely (``index.pkl``) must be rebuilt by re-running ``ingest.py``.

``langchain-community`` is deliberately not used here (it is sunset and its
FAISS wrapper requires ``allow_dangerous_deserialization=True``).
"""

import json
import uuid
from pathlib import Path

_INDEX_FAISS_FILE = "index.faiss"
_INDEX_SAFE_FILE = "index.safe.json"

_DEFAULT_TOP_K = 4


class RagIndexError(RuntimeError):
    pass


class _InMemoryDocstore:
    """Minimal in-memory docstore (id -> Document dict)."""

    def __init__(self, dictionary=None):
        self._dict = dictionary or {}


def _dependable_faiss():
    import faiss

    return faiss


class _FaissVectorStore:
    """Minimal FAISS store exposing the surface used by this gateway."""

    def __init__(self, embedding_function, index, docstore, index_to_docstore_id, vectors=None):
        self.embedding_function = embedding_function
        self.index = index
        self.docstore = docstore
        self.index_to_docstore_id = index_to_docstore_id
        self._vectors = vectors

    @classmethod
    def from_documents(cls, documents, embedding):
        import numpy as np

        if not documents:
            raise ValueError("No documents to index — the FAISS store cannot be empty.")
        faiss_lib = _dependable_faiss()
        vectors = embedding.embed_documents([doc.page_content for doc in documents])
        vectors_array = np.asarray(vectors, dtype="float32")
        index = faiss_lib.IndexIDMap(faiss_lib.IndexFlatL2(vectors_array.shape[1]))
        docstore_dict = {}
        index_to_docstore_id = {}
        for position, doc in enumerate(documents):
            doc_id = uuid.uuid4().hex
            docstore_dict[doc_id] = doc
            index_to_docstore_id[position] = doc_id
        index.add_with_ids(vectors_array, np.arange(len(documents), dtype="int64"))
        return cls(
            embedding,
            index,
            _InMemoryDocstore(docstore_dict),
            index_to_docstore_id,
            vectors=vectors_array,
        )

    def _query_vector(self, query):
        import numpy as np

        return np.asarray(self.embedding_function.embed_query(query), dtype="float32")

    def _documents_for_ids(self, index_ids):
        documents = []
        for index_id in index_ids:
            if int(index_id) not in self.index_to_docstore_id:
                continue
            doc_id = self.index_to_docstore_id[int(index_id)]
            documents.append(self.docstore._dict[doc_id])
        return documents

    def similarity_search(self, query, k=_DEFAULT_TOP_K):
        query_vector = self._query_vector(query).reshape(1, -1)
        _, index_ids = self.index.search(query_vector, k)
        return self._documents_for_ids(index_ids[0])

    def similarity_search_with_scores(self, query, k=_DEFAULT_TOP_K):
        """Return ``(document, squared_l2_distance)`` pairs, best first."""
        query_vector = self._query_vector(query).reshape(1, -1)
        distances, index_ids = self.index.search(query_vector, k)
        results = []
        for position, index_id in enumerate(index_ids[0]):
            if int(index_id) not in self.index_to_docstore_id:
                continue
            doc_id = self.index_to_docstore_id[int(index_id)]
            doc = self.docstore._dict[doc_id]
            results.append((doc, float(distances[0][position])))
        return results


def _doc_to_payload(doc) -> dict:
    return {"page_content": doc.page_content, "metadata": doc.metadata}


def save_local_safe(store, folder: str) -> None:
    """Persist a FAISS index without pickle: binary index + JSON docstore."""
    faiss_lib = _dependable_faiss()
    index_dir = Path(folder)
    index_dir.mkdir(parents=True, exist_ok=True)
    faiss_lib.write_index(store.index, str(index_dir / _INDEX_FAISS_FILE))
    payload = {
        "docstore": {key: _doc_to_payload(doc) for key, doc in store.docstore._dict.items()},
        "index_to_docstore_id": {str(k): v for k, v in store.index_to_docstore_id.items()},
    }
    if store._vectors is not None:
        payload["vectors"] = [list(map(float, vector)) for vector in store._vectors]
    (index_dir / _INDEX_SAFE_FILE).write_text(
        json.dumps(payload, ensure_ascii=False, default=str), encoding="utf-8"
    )


def load_local_safe(folder: str, embeddings):
    """Rebuild a FAISS store from the safe JSON-serialized files."""
    from langchain_core.documents import Document

    faiss_lib = _dependable_faiss()
    index_dir = Path(folder)
    payload = json.loads((index_dir / _INDEX_SAFE_FILE).read_text(encoding="utf-8"))
    docstore = _InMemoryDocstore(
        {
            key: Document(page_content=value["page_content"], metadata=value["metadata"])
            for key, value in payload["docstore"].items()
        }
    )
    index_to_docstore_id = {int(k): v for k, v in payload["index_to_docstore_id"].items()}
    vectors = payload.get("vectors")
    if vectors is not None:
        import numpy as np

        vectors_array = np.asarray(vectors, dtype="float32")
    else:
        vectors_array = None
    return _FaissVectorStore(
        embedding_function=embeddings,
        index=faiss_lib.read_index(str(index_dir / _INDEX_FAISS_FILE)),
        docstore=docstore,
        index_to_docstore_id=index_to_docstore_id,
        vectors=vectors_array,
    )


def load_vector_store(index_dir: str, embeddings):
    """Load a FAISS index safely only (refuses pickle-based indices)."""
    index_dir = Path(index_dir)
    if not (index_dir / _INDEX_FAISS_FILE).is_file():
        raise RagIndexError(f"Index not found in {index_dir} — run ingest.py to build it.")
    if not (index_dir / _INDEX_SAFE_FILE).is_file():
        raise RagIndexError(
            "The FAISS index was serialized unsafely (pickle). Rebuild it by running ingest.py."
        )
    try:
        return load_local_safe(str(index_dir), embeddings)
    except Exception as exc:  # noqa: BLE001 — surface a user-facing message
        raise RagIndexError(
            "Corrupt or unreadable index — rebuild it by running ingest.py."
        ) from exc

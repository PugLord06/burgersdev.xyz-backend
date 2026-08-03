import os
import urllib.request
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from app.config import DB_PATH, EMBEDDING_MODEL, OLLAMA_BASE_URL

# Module-level cache to avoid re-initializing on every request
_cached_embeddings: Embeddings | None = None
_cached_vectorstore: Chroma | None = None


class ChromaDefaultEmbeddings(Embeddings):
    """Fallback embedding engine using ChromaDB ONNX MiniLM embeddings."""

    def __init__(self):
        import chromadb.utils.embedding_functions as ef
        self._ef = ef.DefaultEmbeddingFunction()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[float(x) for x in vec] for vec in self._ef(texts)]

    def embed_query(self, text: str) -> list[float]:
        return [float(x) for x in self._ef([text])[0]]


def get_embedding_function() -> Embeddings:
    global _cached_embeddings
    if _cached_embeddings is not None:
        return _cached_embeddings

    # On Cloud Run (K_SERVICE is set), Ollama is never available — skip the probe
    if not os.environ.get("K_SERVICE"):
        try:
            url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/tags"
            req = urllib.request.urlopen(url, timeout=0.2)
            if req.status == 200:
                _cached_embeddings = OllamaEmbeddings(
                    model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL
                )
                return _cached_embeddings
        except Exception:
            pass

    _cached_embeddings = ChromaDefaultEmbeddings()
    return _cached_embeddings


def get_vectorstore(db_path: str = None):
    global _cached_vectorstore
    target_db = db_path or DB_PATH
    if _cached_vectorstore is not None:
        return _cached_vectorstore
    embeddings = get_embedding_function()
    _cached_vectorstore = Chroma(
        persist_directory=target_db, embedding_function=embeddings
    )
    return _cached_vectorstore


def get_retriever(db_path: str = None, k: int = 3):
    vs = get_vectorstore(db_path)
    return vs.as_retriever(search_kwargs={"k": k})

import urllib.request
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from app.config import DB_PATH, EMBEDDING_MODEL, OLLAMA_BASE_URL


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
    try:
        url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/tags"
        req = urllib.request.urlopen(url, timeout=0.2)
        if req.status == 200:
            return OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
    except Exception:
        pass
    return ChromaDefaultEmbeddings()


def get_vectorstore(db_path: str = None):
    target_db = db_path or DB_PATH
    embeddings = get_embedding_function()
    return Chroma(persist_directory=target_db, embedding_function=embeddings)


def get_retriever(db_path: str = None, k: int = 3):
    vs = get_vectorstore(db_path)
    return vs.as_retriever(search_kwargs={"k": k})

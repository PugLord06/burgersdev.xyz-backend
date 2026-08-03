import os
import time
import subprocess
import urllib.request
from langchain_community.vectorstores import Chroma
from app.config import DATA_PATH, DB_PATH, OLLAMA_BASE_URL, OLLAMA_EXE_PATH
from app.services.document_loader import load_and_split_documents
from app.db.vectorstore import get_embedding_function


def check_and_start_ollama(url: str = OLLAMA_BASE_URL, exe_path: str = OLLAMA_EXE_PATH) -> bool:
    """Verify connection to Ollama, attempting to launch executable if present."""
    target_url = f"{url.rstrip('/')}/api/tags"
    try:
        req = urllib.request.urlopen(target_url, timeout=0.2)
        if req.status == 200:
            return True
    except Exception:
        pass

    if os.path.exists(exe_path):
        try:
            subprocess.Popen([exe_path, "app"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for _ in range(3):
                time.sleep(0.5)
                try:
                    req = urllib.request.urlopen(target_url, timeout=0.2)
                    if req.status == 200:
                        return True
                except Exception:
                    pass
        except Exception:
            pass
    return False


def run_ingestion(data_path: str = None, db_path: str = None) -> int:
    """Execute document loading, text splitting, embedding generation, and vector store population."""
    target_data = data_path or DATA_PATH
    target_db = db_path or DB_PATH

    check_and_start_ollama()

    chunks = load_and_split_documents(target_data)
    embeddings = get_embedding_function()
    
    existing_vs = Chroma(persist_directory=target_db, embedding_function=embeddings)
    try:
        existing_vs.delete_collection()
    except Exception:
        pass

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=target_db
    )
    return len(chunks)


def ingest_data(data_path: str = None, db_path: str = None) -> int:
    """Alias for run_ingestion for backward compatibility with PROJECT.md interface contract."""
    return run_ingestion(data_path, db_path)

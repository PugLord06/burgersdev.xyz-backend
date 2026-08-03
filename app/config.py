import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.environ.get("DATA_PATH", os.path.join(BASE_DIR, "data", "resume.txt"))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "chroma_db"))

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "nomic-embed-text")
LLM_MODEL = os.environ.get("LLM_MODEL", "llama3.2")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", "50"))
OLLAMA_EXE_PATH = os.environ.get(
    "OLLAMA_EXE_PATH",
    r"C:\Users\cosmi\AppData\Local\Programs\Ollama\ollama.exe"
)

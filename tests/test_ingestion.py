import os
import shutil
import tempfile
import pytest
from app.services.ingest_service import ingest_data
from app.services.document_loader import load_and_split_documents
from app.db.vectorstore import get_vectorstore, get_retriever
from app.config import DATA_PATH

def test_tier1_ingestion_execution():
    """Tier 1: Verify ingestion execution on default resume data."""
    chunk_count = ingest_data()
    assert isinstance(chunk_count, int)
    assert chunk_count > 0, "Ingestion should produce at least 1 document chunk."

def test_tier1_chromadb_creation():
    """Tier 1: Verify ChromaDB vector store creation and persistence."""
    temp_dir = tempfile.mkdtemp()
    try:
        count = ingest_data(data_path=DATA_PATH, db_path=temp_dir)
        assert count > 0
        assert os.path.exists(temp_dir), "ChromaDB directory should be created."
        vs = get_vectorstore(db_path=temp_dir)
        assert vs is not None
        retriever = get_retriever(db_path=temp_dir, k=2)
        assert retriever is not None
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def test_tier2_custom_path_ingestion():
    """Tier 2: Verify ingestion with custom document file and database path."""
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt", encoding="utf-8") as tmp_file:
        tmp_file.write("Custom candidate profile.\nSkills: Python, Docker, PyTest.")
        tmp_file_path = tmp_file.name

    temp_db_dir = tempfile.mkdtemp()
    try:
        chunk_count = ingest_data(data_path=tmp_file_path, db_path=temp_db_dir)
        assert chunk_count == 1
        retriever = get_retriever(db_path=temp_db_dir, k=1)
        results = retriever.invoke("Python")
        assert len(results) > 0
        assert "Python" in results[0].page_content
    finally:
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
        shutil.rmtree(temp_db_dir, ignore_errors=True)

def test_tier2_missing_file_handling():
    """Tier 2: Verify error raised when document path is invalid."""
    fake_path = os.path.join(tempfile.gettempdir(), "non_existent_resume_12345.txt")
    with pytest.raises(FileNotFoundError):
        load_and_split_documents(fake_path)

import os
import glob
import importlib
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _get_all_python_files():
    py_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        if ".venv" in root or ".git" in root or ".agents" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def test_tier2_loc_limit_per_python_file():
    """Tier 2: Verify strictly < 150 lines of code per Python file in repository."""
    py_files = _get_all_python_files()
    assert len(py_files) > 0, "No python files found to test."

    violations = []
    for filepath in py_files:
        rel_path = os.path.relpath(filepath, ROOT_DIR)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        line_count = len(lines)
        if line_count >= 150:
            violations.append(f"{rel_path}: {line_count} LOC (Limit: <150)")

    assert not violations, f"LOC violations detected:\n" + "\n".join(violations)

def test_tier1_interface_contracts():
    """Tier 1: Verify all required interface contracts and module exports exist."""
    ingest_mod = importlib.import_module("app.services.ingest_service")
    assert hasattr(ingest_mod, "ingest_data")

    vs_mod = importlib.import_module("app.db.vectorstore")
    assert hasattr(vs_mod, "get_vectorstore")
    assert hasattr(vs_mod, "get_retriever")

    rag_mod = importlib.import_module("app.services.rag_service")
    assert hasattr(rag_mod, "stream_chat_response")

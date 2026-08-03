import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def load_and_split_documents(data_path: str = None) -> List[Document]:
    target_path = data_path or DATA_PATH
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Document file not found at {target_path}")

    loader = TextLoader(target_path, encoding="utf-8")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(docs)

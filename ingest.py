import sys
from app.services.ingest_service import run_ingestion


def main():
    count = run_ingestion()
    print(f"Successfully ingested {count} chunks.")


if __name__ == "__main__":
    main()

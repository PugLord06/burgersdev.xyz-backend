import asyncio
import json
import os
from typing import AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from app.db.vectorstore import get_retriever

async def stream_chat_response(query: str, db_path: str = None) -> AsyncGenerator[str, None]:
    try:
        retriever = get_retriever(db_path=db_path, k=3)
        docs = retriever.invoke(query)
    except Exception:
        docs = []

    yielded_any = False
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY is not set or invalid.")

        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
        context_str = "\n---\n".join([doc.page_content for doc in docs]) if docs else ""
        prompt = f"Context:\n{context_str}\n\nQuestion: {query}\n\nAnswer:"
        
        for chunk in llm.stream(prompt):
            payload = json.dumps({"content": chunk.content})
            yield f"data: {payload}\n\n"
            yielded_any = True
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        pass

    if not yielded_any:
        # Fallback if Gemini fails or API key is missing
        answer = "⚠️ **AI Backend Offline or Misconfigured**\n\nI am currently unable to reach the Gemini AI servers. Please ensure the GEMINI_API_KEY is set in the backend environment."
        chunk_size = 4
        for i in range(0, len(answer), chunk_size):
            chunk = answer[i:i+chunk_size]
            payload = json.dumps({"content": chunk})
            yield f"data: {payload}\n\n"
            await asyncio.sleep(0.005)

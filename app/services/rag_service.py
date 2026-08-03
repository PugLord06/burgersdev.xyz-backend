import asyncio
import json
import os
import traceback
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
    last_error = ""

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY environment variable is missing or set to placeholder.")

        llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash", 
            google_api_key=api_key,
            temperature=0.7
        )
        
        context_str = "\n---\n".join([doc.page_content for doc in docs]) if docs else ""
        prompt = f"Context:\n{context_str}\n\nQuestion: {query}\n\nAnswer:"
        
        async for chunk in llm.astream(prompt):
            raw_content = chunk.content
            extracted_text = ""
            
            if isinstance(raw_content, str):
                extracted_text = raw_content
            elif isinstance(raw_content, list):
                for part in raw_content:
                    if isinstance(part, str):
                        extracted_text += part
                    elif isinstance(part, dict):
                        if part.get("type") == "text" and "text" in part:
                            extracted_text += part["text"]
                        elif "text" in part and isinstance(part["text"], str):
                            extracted_text += part["text"]
            
            if extracted_text:
                payload = json.dumps({"content": extracted_text})
                yield f"data: {payload}\n\n"
                yielded_any = True
                await asyncio.sleep(0.001)
    except Exception as e:
        last_error = f"{type(e).__name__}: {str(e)}"
        print(f"Gemini API Error: {last_error}\n{traceback.format_exc()}")

    if not yielded_any:
        error_details = last_error if last_error else "Unknown initialization error"
        answer = f"⚠️ **AI Backend Error**\n\nFailed to get response from Gemini API.\n**Details:** `{error_details}`"
        chunk_size = 4
        for i in range(0, len(answer), chunk_size):
            chunk = answer[i:i+chunk_size]
            payload = json.dumps({"content": chunk})
            yield f"data: {payload}\n\n"
            await asyncio.sleep(0.005)

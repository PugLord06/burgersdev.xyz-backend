# Portfolio AI Backend 🤖⚡

A high-performance, asynchronous RAG (Retrieval-Augmented Generation) microservice built with **FastAPI**, **LangChain**, and **ChromaDB**, deployed on **Google Cloud Run**.

It powers the interactive AI Assistant for [Michael Burgers' Portfolio](https://burgersportfolio.web.app), allowing recruiters and visitors to query professional experience, technical stacks, and project details in real-time.

---

## 🌟 Key Features

* **⚡ Real-Time Streaming:** Server-Sent Events (SSE) stream responses character-by-character for zero perceived latency.
* **🧠 Retrieval-Augmented Generation (RAG):** Contextually fetches relevant resume and project data using **ChromaDB** vector storage.
* **🔒 Production Security:**
  * **Strict CORS:** Locked down to authorized domains (`burgersportfolio.web.app`).
  * **Rate Limiting:** Integrated `SlowAPI` limiting each IP to 5 requests per minute to prevent token abuse.
* **☁️ Cloud-Native Deployment:** Containerized with Docker and continuously deployed to **Google Cloud Run**.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python 3.11)
* **LLM Orchestration:** LangChain (`langchain-google-genai`)
* **AI Model:** Google Gemini API (`gemini-3.5-flash`)
* **Vector Database:** ChromaDB (ONNX MiniLM Embeddings)
* **Rate Limiting:** SlowAPI
* **Server:** Uvicorn (ASGI)

---

## 🚀 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PugLord06/burgersdev.xyz-backend.git
   cd burgersdev.xyz-backend
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file based on `.env.example`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the API server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`.

---

## 🐳 Docker Setup

Build and run locally with Docker:
```bash
docker build -t portfolio-ai-backend .
docker run -p 8080:8080 -e GEMINI_API_KEY="your_api_key" portfolio-ai-backend
```

---

## 📜 License

MIT © [Michael Burgers](https://github.com/PugLord06)

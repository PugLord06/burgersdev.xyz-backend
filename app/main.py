from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.dependencies import limiter
from app.api.chat_router import router as chat_router

app = FastAPI(title="Portfolio AI Backend", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:4173",
        "https://burgersportfolio.web.app",
        "https://burgersportfolio.firebaseapp.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/")
def root():
    return {"status": "online", "service": "portfolio-ai-backend"}

@app.get("/health")
def health():
    return {"status": "healthy"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="STEM-Notes AI",
    description="Agentic RAG Backend for high-fidelity STEM note-taking.",
    version="0.1.0"
)

# Enable CORS for frontend or browser extension connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "STEM-Notes AI API is online",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
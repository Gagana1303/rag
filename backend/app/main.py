from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload, query
from app.db.qdrant_client import create_collections
import os
from dotenv import load_dotenv

load_dotenv()

# ================================
# 1. CREATE APP
# ================================

app = FastAPI(
    title="Scripture RAG API",
    description="RAG-based system for Mahabharata, Ramayana, and Puranas",
    version="1.0.0"
)


# ================================
# 2. ENABLE CORS (IMPORTANT)
# ================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # IMPORTANT
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# 3. STARTUP EVENT
# ================================

@app.on_event("startup")
def startup_event():
    print("🚀 Starting Scripture RAG Backend...")
    create_collections()
    print("✅ Qdrant collections ready")


# ================================
# 4. REGISTER ROUTES
# ================================

app.include_router(upload.router, prefix="/api")
app.include_router(query.router, prefix="/api")


# ================================
# 5. ROOT CHECK
# ================================

@app.get("/")
def home():
    return {"message": "Scripture RAG Backend Running 🚀"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload, query
from app.db.qdrant_client import create_collections


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
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://10.175.194.15:3000",  # ✅ ADD THIS
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # IMPORTANT
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
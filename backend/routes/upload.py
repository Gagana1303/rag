from fastapi import APIRouter, UploadFile, Form, HTTPException
import os
import hashlib
from fastapi import BackgroundTasks
from app.services.extractor import extract_text
from app.services.cleaner import clean_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_chunks
from app.services.rag_pipeline import store_in_qdrant

router = APIRouter()

UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# store hashes in memory (simple & safe)
uploaded_hashes = set()
processing_status = {}

def generate_hash(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()

def process_file(file_path, scripture, section, file_hash):

    processing_status[file_hash] = "processing"

    try:
        text = extract_text(file_path)

        if not text or len(text.strip()) < 50:
            processing_status[file_hash] = "failed"
            return

        text = clean_text(text)
        chunks = chunk_text(text)

        if not chunks:
            processing_status[file_hash] = "failed"
            return

        vectors = embed_chunks(chunks)

        metadata = {
            "scripture": scripture.lower(),
            "section": section,
        }

        store_in_qdrant(scripture.lower(), chunks, vectors, metadata)

        uploaded_hashes.add(file_hash)

        processing_status[file_hash] = "completed"

    except Exception as e:
        print("❌ Background error:", e)
        processing_status[file_hash] = "failed"

@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    scripture: str = Form(...),
    section: str = Form(...)
):

    allowed = (".pdf", ".txt", ".docx")

    if not file.filename.lower().endswith(allowed):
        raise HTTPException(
        status_code=400,
        detail="Only PDF, TXT, DOCX supported"
    )
    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file")

        file_hash = generate_hash(file_bytes)

        if file_hash in uploaded_hashes:
            raise HTTPException(
                status_code=400,
                detail="⚠️ This file is already uploaded!"
            )

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # 🚀 Run processing in background
        background_tasks.add_task(
            process_file,
            file_path,
            scripture,
            section,
            file_hash
        )

        return {
    "message": "File uploaded. Processing started.",
    "file_id": file_hash   # 🔥 IMPORTANT
}

    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{file_id}")
def get_status(file_id: str):
    status = processing_status.get(file_id, "unknown")
    return {"status": status}

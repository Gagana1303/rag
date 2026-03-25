from fastapi import APIRouter, UploadFile, Form
import os

from app.services.extractor import extract_text
from app.services.cleaner import clean_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_chunks
from app.services.rag_pipeline import store_in_qdrant

router = APIRouter()

UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    scripture: str = Form(...),
    section: str = Form(...)
):

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    scripture = scripture.lower()

    # Step 1: Extract
    text = extract_text(file_path)

    # Step 2: Clean
    text = clean_text(text)

    # Step 3: Chunk
    chunks = chunk_text(text)

    # Step 4: Embed
    vectors = embed_chunks(chunks)

    # Step 5: Store
    metadata = {
        "scripture": scripture,
        "section": section
    }

    store_in_qdrant(scripture, chunks, vectors, metadata)

    return {
        "message": "File processed successfully",
        "chunks": len(chunks)
    }
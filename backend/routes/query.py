from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_pipeline import rag_query

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    scripture: str


@router.post("/ask")
async def ask_question(request: QueryRequest):

    # 🔥 Use your RAG pipeline
    answer, results = rag_query(
        question=request.question,
        scripture=request.scripture.lower()
    )

    return {
        "answer": answer
    }
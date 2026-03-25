from app.db.qdrant_client import client
from app.services.embedder import embed_chunks, embed_query
from qdrant_client.models import PointStruct
import uuid
import ollama
from google import genai
from app.config import GOOGLE_API_KEY
from qdrant_client import QdrantClient



genai_client = genai.Client(api_key=GOOGLE_API_KEY)

def store_in_qdrant(collection, chunks, vectors, metadata):

    points = []

    for i in range(len(chunks)):

        payload = {
            "text": chunks[i],
            "chunk_index": i,
            **metadata
        }

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vectors[i],
                payload=payload
            )
        )

    client.upsert(
        collection_name=collection,
        points=points
    )


# ================================
# 2. SEARCH QDRANT
# ================================

def search_qdrant(scripture, question):
    query_vector = embed_query(question)

    results = client.query_points(
    collection_name=scripture,
    query=query_vector,
    limit=5
)

    return results.points


# ================================
# 3. BUILD CONTEXT
# ================================

def build_context(results):
    context = ""

    for r in results:
        if "text" in r.payload:
            context += r.payload["text"] + "\n\n"

    return context[:2000]  # limit size


# ================================
# 4. GENERATE ANSWER
# ================================

def build_prompt(context, question):
    return f"""
You are a knowledgeable assistant specialized in answering questions from religious scriptures.

STRICT RULES:
1. Answer ONLY from the provided context.
2. Do NOT use outside knowledge.
3. If answer is not in context, say:
   "The answer is not available in the provided text."
4. Keep answers clear and meaningful.
5. If possible, include names, roles, and relationships.

---------------------
CONTEXT:
{context}
---------------------

QUESTION:
{question}

ANSWER:
"""


def generate_answer(context, question):
    prompt = build_prompt(context, question)

    response = ollama.chat(
        model="phi",   # change if needed
        messages=[
            {"role": "system", "content": "You are a scripture expert."},
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 0.3,   # low = more factual
            "top_p": 0.9,
            "num_predict": 300    # limit response size
        }
    )

    return response["message"]["content"]

# ================================
# 5. MAIN PIPELINE
# ================================

def rag_query(question, scripture):

    # Step 1: Retrieve
    results = search_qdrant(scripture, question)

    # Step 2: Build context
    context = build_context(results)

    # Step 3: Generate answer
    answer = generate_answer(context, question)
    return answer, results
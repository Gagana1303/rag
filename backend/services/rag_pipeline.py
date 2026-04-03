from app.db.qdrant_client import client
from app.services.embedder import embed_query
from qdrant_client.models import PointStruct
import uuid
from groq import Groq
from app.config import GROQ_API_KEY

groq_client = Groq(api_key=GROQ_API_KEY)


# ================================
# 1. STORE IN QDRANT
# ================================
def store_in_qdrant(collection, chunks, vectors, metadata):

    from app.db.qdrant_client import client
    from qdrant_client.models import PointStruct
    import uuid

    BATCH_SIZE = 100   # 🔥 critical

    total = len(chunks)
    print(f"📦 Total chunks: {total}")

    for i in range(0, total, BATCH_SIZE):
        batch_chunks = chunks[i:i+BATCH_SIZE]
        batch_vectors = vectors[i:i+BATCH_SIZE]

        points = []

        for j in range(len(batch_chunks)):
            payload = {
                "text": batch_chunks[j],
                "chunk_index": i + j,
                **metadata
            }

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=batch_vectors[j],
                    payload=payload
                )
            )

        print(f"🚀 Uploading batch {i} → {i+len(points)}")

        client.upsert(
            collection_name=collection,
            points=points
        )

    print("✅ All batches stored successfully")

# ================================
# 2. SEARCH QDRANT (IMPROVED 🔥)
# ================================
def search_qdrant(scripture, question):

    query_vector = embed_query(question)

    results = client.query_points(
        collection_name=scripture,
        query=query_vector,
        limit=10
    )

    points = results.points

    # 🔥 sort by similarity score
    points = sorted(points, key=lambda x: x.score, reverse=True)

    # 🔥 filter weak matches (VERY IMPORTANT)
    points = [p for p in points if p.score > 0.6]

    return points[:4]


# ================================
# 3. BUILD CONTEXT
# ================================
def build_context(results):

    context = "\n\n".join([
        r.payload["text"]
        for r in results
        if "text" in r.payload
    ])

    return context[:2000]


# ================================
# 4. PROMPT
# ================================
def build_prompt(context, question):
    return f"""
You are a STRICT retrieval-based assistant specialized ONLY in answering questions from Hindu scriptures such as the Mahabharata and Ramayana.

=====================
CRITICAL INSTRUCTIONS
=====================
1. You MUST answer ONLY using the provided CONTEXT.
2. You MUST NOT use any external knowledge.
3. You MUST NOT mention other religions (like Bible, Christianity, etc.).
4. You MUST NOT behave like a general AI assistant.
5. DO NOT explain your limitations.
6. DO NOT add assumptions or imagination.

=====================
ANSWER RULES
=====================
- If answer is clearly present → give a direct answer.
- If partially present → answer only what is supported by context.

=====================
STYLE
=====================
- Maximum 7-9 sentences
- Clear and factual
- No introduction (NO: "According to the text...")
- No extra explanation
- Include names and roles if present

=====================
CONTEXT
=====================
\"\"\"
{context}
\"\"\"

=====================
QUESTION
=====================
{question}

=====================
FINAL ANSWER
=====================
"""

# ================================
# 5. GENERATE ANSWER (GROQ 🔥)
# ================================
def generate_answer(context, question):



    prompt = build_prompt(context, question)

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Strict RAG assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=200
    )

    return response.choices[0].message.content


# ================================
# 6. MAIN PIPELINE
# ================================
def rag_query(question, scripture):

    results = search_qdrant(scripture, question)

    context = build_context(results)

    answer = generate_answer(context, question)

    return answer, results

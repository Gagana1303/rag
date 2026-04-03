from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.config import QDRANT_URL, QDRANT_API_KEY
from qdrant_client import QdrantClient


client = QdrantClient(
    url=QDRANT_URL.strip(),   # 🔥 removes hidden spaces
    api_key=QDRANT_API_KEY,
    timeout=120,
    check_compatibility=False
)

def create_collections():

    collections = ["mahabharata", "ramayana", "puranas"]

    for col in collections:

        if not client.collection_exists(col):
            client.create_collection(
                collection_name=col,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

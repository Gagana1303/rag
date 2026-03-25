from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient("http://localhost:6333")

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
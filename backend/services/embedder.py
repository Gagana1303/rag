from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks):
    """
    Input: List of text chunks
    Output: List of embeddings (vectors)
    """
    embeddings = model.encode(chunks)
    return [vec.tolist() for vec in embeddings]


def embed_query(text):
    """
    Input: Single query string
    Output: Single embedding vector
    """
    return model.encode(text).tolist()
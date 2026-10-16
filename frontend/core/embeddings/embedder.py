from sentence_transformers import SentenceTransformer


# Free embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():
    """Load the local embedding model."""
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(texts: list[str]):
    """Convert a list of text chunks into vectors."""
    model = load_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors
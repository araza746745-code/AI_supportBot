import faiss
import numpy as np


class VectorStore:
    """Store text embeddings and search for similar vectors."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.texts = []

    def add(self, texts: list[str], embeddings):
        """Add text chunks and their embeddings."""
        vectors = np.asarray(embeddings, dtype="float32")

        if len(texts) != len(vectors):
            raise ValueError("Texts and embeddings must have equal lengths.")

        if vectors.ndim != 2 or vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected vectors with {self.dimension} dimensions."
            )

        if not texts:
            return

        self.index.add(vectors)
        self.texts.extend(texts)

    def search(self, query_embedding, top_k: int = 3):
        """Return the most similar text chunks."""
        if not self.texts or top_k <= 0:
            return []

        vector = np.asarray(
            query_embedding, dtype="float32"
        ).reshape(1, -1)

        if vector.shape[1] != self.dimension:
            raise ValueError("Query embedding has the wrong dimension.")

        scores, indices = self.index.search(
            vector, min(top_k, len(self.texts))
        )

        return [
            {"text": self.texts[i], "score": float(score)}
            for score, i in zip(scores[0], indices[0])
            if i >= 0
        ]
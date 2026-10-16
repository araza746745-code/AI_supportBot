from vector_store import VectorStore
import numpy as np


store = VectorStore(dimension=3)

texts = [
    "Python is a programming language",
    "The sky is blue",
    "Machine learning uses data",
]

embeddings = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.9, 0.1, 0.0],
], dtype="float32")

store.add(texts, embeddings)

query = np.array([1.0, 0.0, 0.0], dtype="float32")

results = store.search(query, top_k=2)

print("Vector search successful!")
for result in results:
    print(result)
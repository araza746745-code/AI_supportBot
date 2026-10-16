from embedder import create_embeddings

texts = [
    "Python is a programming language.",
    "A dog is an animal.",
    "Python is used for AI and machine learning."
]

vectors = create_embeddings(texts)

print("Embeddings created successfully!")
print("Number of texts:", len(texts))
print("Vector shape:", vectors.shape)
print("First vector (first 10 numbers):", vectors[0][:10])
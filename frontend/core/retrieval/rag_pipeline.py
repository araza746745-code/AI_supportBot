import requests

from core.document_processor.loader import load_pdf
from core.document_processor.chunker import split_text
from core.embeddings.embedder import create_embeddings
from core.retrieval.vector_store import VectorStore


def build_rag_pipeline(pdf_path: str, question: str, top_k: int = 3):
    """Answer a user's question using relevant PDF content."""

    # 1. Read PDF
    pdf_text = load_pdf(pdf_path)

    if not pdf_text.strip():
        raise ValueError("No readable text found in the PDF.")

    # 2. Split PDF text into chunks
    chunks = split_text(pdf_text, chunk_size=500, overlap=50)

    # 3. Create embeddings
    vectors = create_embeddings(chunks)

    # 4. Store vectors and text
    store = VectorStore(dimension=vectors.shape[1])
    store.add(chunks, vectors)

    # 5. Search for relevant text
    question_vector = create_embeddings([question])[0]
    results = store.search(question_vector, top_k=top_k)

    # 6. Prepare context
    context = "\n\n".join(
        result["text"] for result in results
    )

    # 7. Ask Ollama to generate an answer
    prompt = f"""
Answer the question using only the context below.
If the answer is not in the context, say you could not find it in the PDF.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    answer = response.json()["response"]

    return answer


if __name__ == "__main__":
    pdf_path = input("Enter PDF path: ").strip().strip('"')
    question = input("Ask a question about the PDF: ").strip()

    try:
        answer = build_rag_pipeline(pdf_path, question)
        print("\nAI Answer:")
        print(answer)

    except Exception as error:
        print(f"\nError: {error}")
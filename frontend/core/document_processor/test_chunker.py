from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from core.document_processor.loader import load_pdf
from core.document_processor.chunker import split_text

pdf_path = PROJECT_ROOT / "simple.pdf"

# Step 1: Read text from PDF
pdf_text = load_pdf(str(pdf_path))

# Step 2: Split PDF text into chunks
chunks = split_text(pdf_text, chunk_size=500, overlap=50)

print("PDF loaded successfully!")
print("Total characters:", len(pdf_text))
print("Total chunks:", len(chunks))

if chunks:
    print("\nFirst chunk:")
    print(chunks[0])
    print("\nFirst chunk length:", len(chunks[0]))
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from core.document_processor.loader import load_pdf

pdf_path = PROJECT_ROOT / "simple.pdf"
pdf_text = load_pdf(str(pdf_path))

print("PDF text extracted successfully!")
print(pdf_text[:1000])
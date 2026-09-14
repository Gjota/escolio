from pathlib import Path
from pypdf import PdfReader
from typing import Protocol
import hashlib

from escolio.models import Document, PageText


class TextExtractor(Protocol):
    """Contract for turning a file into its pages of text"""
    def extract(self, path: Path) -> list[PageText]: ...


class PdfExtractor:
    """Extracts text from PDF files. Satisfies TextExtractor"""
    def extract(self, pdf_path: Path) -> list[PageText]:
        reader = PdfReader(pdf_path)
        pages: list[PageText] = []
        for num_pag, page in enumerate(reader.pages, start=1):
            pages.append(
                PageText(page_number=num_pag,
                         text=page.extract_text() or "")
            )
        return pages


def load_document(path: Path, extractor: TextExtractor) -> Document:
    """Builds a document from a file, using the given extractor"""
    document = Document(
        doc_id=hashlib.sha256(path.read_bytes()).hexdigest(),
        original_path=path,
        pages=tuple(extractor.extract(path))
        )
    return document


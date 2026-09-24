from pathlib import Path

from escolio.ingest import PdfExtractor, load_folder
from escolio.models import Document

# Ruta del propio fichero → scripts/ → raíz del repositorio.
# __file__ es la ruta de este .py; resolve() la hace absoluta;
# cada .parent sube un nivel.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "papers"       # el / concatena rutas
OUTPUT_FILE = PROJECT_ROOT / "data" / "extracted_text.txt"


def format_documents(documents: tuple[Document, ...]) -> str:
    """Renders documents as plain text with page markers.
    Pure: takes data, returns text, touches no files."""
    parts: list[str] = []
    for i, document in enumerate(documents, start=1):
        parts.append(f"===== Document {i} — {document.original_path.name} =====")
        for page in document.pages:
            parts.append(f"----- page {page.page_number} -----")
            parts.append(page.text)
    return "\n".join(parts)


def main() -> None:
    """Entry point: loads the corpus, writes the dump, reports what happened."""
    report = load_folder(DOCUMENTS_DIR, PdfExtractor())

    text = format_documents(report.documents)
    OUTPUT_FILE.write_text(text, encoding="utf-8")

    print(f"{len(report.documents)} loaded, {len(report.failures)} failed")
    for failure in report.failures:
        print(f"  failed: {failure.path.name} — {failure.reason}")

    print(f"written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
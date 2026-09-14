from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen=True)
class PageText:
    page_number: int
    text: str


@dataclass(frozen=True)
class Document:
    doc_id: str #SHA-256 of the content
    original_path: Path
    pages: tuple[PageText, ...]

    @property
    def page_count(self) -> int:
        return len(self.pages)


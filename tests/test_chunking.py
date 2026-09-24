from escolio.chunking import normalize, join_pages
from escolio.models import Document, PageText
from pathlib import Path

def test_joins_hyphenated_line_break() -> None:
    assert normalize("mo-\nments") == "moments"

def test_joins_hyphenated_line_break_with_trailing_space() -> None:
    assert normalize("mo- \nments") == "moments"

def test_does_not_join_hyphen_across_blank_line() -> None:
    assert normalize("mo- \n\n\nments") == "mo- ments"

def test_leaves_inline_hyphen_untouched() -> None:
    assert normalize("state-of-the-art") == "state-of-the-art"

def test_expands_ligature() -> None:
    assert normalize("\ufb01rst") == "first"


def make_document(texts: list[str]) -> Document:
    """Builds a Document with one page per text, numbered from 1."""
    return Document(
        doc_id="test",
        original_path=Path("test.pdf"),
        pages=tuple(
            PageText(page_number=i, text=t)
            for i, t in enumerate(texts, start=1)
        ),
    )

def test_joins_single_page() -> None:
    document = make_document(["Hello world"])
    assert join_pages(document) == ("Hello world",[0])

def test_joins_two_pages() -> None:
    document = make_document(["Hola mundo", "Adiós"])
    assert join_pages(document) == ("Hola mundo Adiós", [0,11])

def test_joins_empty_pages() -> None:
    document = make_document(["abc","", "efg"])
    assert join_pages(document) == ("abc  efg",[0, 4, 5])

def test_joins_single_empty_page() -> None:
    document = make_document([""])
    assert join_pages(document) == ("",[0])

def test_joins_empty_document() -> None:
    document = make_document([])
    assert join_pages(document) == ("",[])

def test_normalizes_each_page() -> None:
    document = make_document(["Hello wor- \nld", "Goo- \nd bye"])
    assert join_pages(document) == ("Hello world Good bye", [0,12])
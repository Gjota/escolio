from escolio.chunking import normalize

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
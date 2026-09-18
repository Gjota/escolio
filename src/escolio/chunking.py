import re
import unicodedata

# A hyphen splitting a word across lines, only joined when the line break is single.
# A blank line means end of block, where a trailing hyphen is more likely to be punctuation than a split word.
_HYPHEN_LINE_BREAK = re.compile(r"-[ \t]*\r?\n[ \t]*(?=\w)")

# Extracted PDF text carries a line break at every visual line, not at semantic boundaries, so line breaks are collapsed into spaces.
_WHITESPACE = re.compile(r"\s+")

def normalize(text: str) -> str:
    """Prepares extracted text for chunking.
       Applies Unicode NFKC normalisation, rejoins words split by a hyphen at
       a line break, collapses runs of whitespace into single spaces, and
       trims the result.
       Normalisation is conservative to avoid corrupt legitimate text.
       See ADR-0007.
    """
    text = unicodedata.normalize("NFKC", text)
    text = _HYPHEN_LINE_BREAK.sub("", text)
    text = _WHITESPACE.sub(" ", text)
    text = text.strip()
    return text


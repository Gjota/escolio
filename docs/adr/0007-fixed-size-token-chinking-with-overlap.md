# 7. Fixed-size token chunking with overlap

## Status
Accepted

## Context
Retrieval works over fragments of text rather than whole documents. Each
fragment is turned into a single fixed-size embedding, so a fragment
covering several topics produces a vector that averages all of them and
matches none precisely. Fragments also have to fit in the model's context
window, which is measured in tokens.

Extracted PDF text carries line breaks at every visual line of the page,
not at semantic boundaries, and words are hyphenated across line breaks.

Citations identify a fragment by document and page, so a fragment must
carry its origin.

## Decision
Extracted text is normalised before splitting: hyphenated line breaks are
joined back into single words, and whitespace is collapsed.

Text is then split into fixed-size chunks measured in tokens, over the
continuous text of the document, with consecutive chunks overlapping.
Chunk size is 500 tokens with an overlap of 75. Both values are
provisional and are the first parameters to tune against the evaluation
set.

Each chunk carries its text, the identifier of its source document, the
page it starts on, the page it ends on, and its ordinal position within
the document.

## Alternatives considered
- Splitting on document structure (sections, headings): Best where
structure is available. The extracted text carries no structure: headings
are indistinguishable from any other line, and committing to one document
layout would break on any other.

- Splitting on sentence boundaries: Produces clean fragments. Detecting
the end of a sentence is unreliable in papers, where a period may be an
abbreviation, a decimal, or part of a citation.

- Fixed-size chunks without overlap: Cheaper, and produces fewer
fragments. Any passage crossing a boundary is split in every fragment, so
a passage that answers a question may exist nowhere in one piece.

- Semantic splitting (cutting where sentence similarity drops): Cuts
follow meaning rather than length. It costs one embedding per sentence at
index time and published comparisons do not show a consistent gain over
fixed-size chunking with overlap.

## Consequences
Any passage shorter than the overlap appears in full in at least one
chunk. This is a mechanical guarantee about spans of text, not about
ideas: the splitter does not know what a concept is.

Overlap costs storage and compute. With 500-token chunks and 75 tokens of
overlap, each chunk advances 425 tokens, so covering the same text takes
about 18% more chunks, embeddings, and rows.

Measuring size in tokens ties chunking to a tokeniser, which belongs to a
specific model family. Changing the embedding model may change what a
chunk of 500 tokens contains.

Chunk boundaries are mechanical, so a chunk may begin or end mid-sentence.
Chunks are never shown to the user verbatim as citations: a citation is a
span selected inside a chunk, which keeps it exact while letting it start
and end at a sensible point.

Changing the chunk size or overlap changes where every boundary falls.
The whole corpus has to be re-chunked and re-embedded, and any evaluation
numbers measured with the previous values are no longer comparable.

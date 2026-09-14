# 3. Faithful extraction, late filtering

## Status
Accepted

## Context
Some pages of a PDF return no text: image-only covers, scanned pages, or
full-page figures.

Citations identify a fragment by page number, and that number has to match
what the user sees when opening the document.

## Decision
The extractor returns every page of the document, including pages that
yield no text, numbered from 1 in the order the viewer displays them.
This is the number the reader sees when opening the file, not any page
number printed in the document itself.

Filtering happens during chunking: a page with no text produces no
chunks.

## Alternatives considered
- Dropping empty pages during extraction: This reduces the amount of
data from the start. If the remaining pages are also renumbered, citations
no longer match the real document and the system loses the only guarantee
it offers.

- Dropping empty pages but keeping their numbers: This avoids the
citation problem, but it places a relevance decision inside the extractor,
which is not its responsibility, and it makes it impossible to later
distinguish an empty page from a page the extractor failed to read.

## Consequences
- Citations always point to the real page number of the document.

- The extractor has a single responsibility and can be verified by comparing
its output against the PDF.

- A page the extractor fails to read is indistinguishable from a page with
no text. Detecting that case, for example to apply OCR, would require
information that is not captured today.

- Pages with no content are kept in memory. This cost is negligible compared
to the risk of losing information in the first stage of the pipeline.
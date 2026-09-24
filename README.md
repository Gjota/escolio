# escolio
 
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)
 
escolio is a RAG system for question answering over a collection of documents.
Each answer comes with the passages it was built from, identified by document
and page, so it can be checked against the original.
 
It runs on local models by default, so the documents never leave your machine.
It can also be configured to use external APIs.
 
**Status:** work in progress. PDF ingestion and text normalisation are done.
Retrieval and answer generation are not built yet.
 
## Motivation
 
I have trained a lot of people, many of them new joiners, and I have had to
learn a new field myself more than once. The same problems come up every
time. Some people don't ask because they are afraid to. Others ask about
everything without looking first. And some spend hours searching the
documentation without finding what they need.
 
escolio is meant to let anyone ask as many questions as they want, find the
answer quickly, and verify it in the source document.
 
It runs locally because most of the documentation I have worked with was
confidential and could not be sent to a third party.
 
## How it works
 
```
Indexing:  PDF -> pages -> normalised text -> chunks -> embeddings -> SQLite
Querying:  question -> embedding -> nearest chunks -> prompt -> answer + citations
```
 
Citations are kept exactly as they appear in the document, never translated
or rewritten, so they can always be found in the original. The answer is
written in the language of the question.
 
If nothing relevant is found, the system says it cannot answer.
 
## Installation
 
Requirements: [uv](https://docs.astral.sh/uv/) and Git.
 
```bash
git clone https://github.com/Gjota/escolio.git
cd escolio
uv sync
```
 
The embedding model is downloaded the first time it is used.
 
## Usage
 
Not available yet. Planned commands:
 
```bash
uv run python -m escolio index ./data/papers
uv run python -m escolio ask "your question"
```
 
## Development
 
```bash
uv run pytest
uv run mypy src
uv run python scripts/dump_text.py   # writes the extracted text to a file for inspection
```
 
## Design decisions
 
Architecture decisions are recorded in [`docs/adr/`](docs/adr/).
 
## Roadmap
 
**v0**
- [x] PDF ingestion with page numbers and content-based document IDs
- [x] Text normalisation
- [ ] Chunking
- [ ] Local embeddings and SQLite storage
- [ ] Retrieval
- [ ] Answers with citations
- [ ] Evaluation set of 35 questions with a reproducible score
**Next**
- HTTP API (FastAPI) and Docker image
- Web interface
- Multiple collections
- More document formats
- Hosted model providers as an option
- Hybrid search (BM25 + embeddings) and reranking
- PostgreSQL with pgvector, once the corpus outgrows in-memory search
## License
 
MIT
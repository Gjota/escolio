# escolio

**Status:** work in progress.

Escolio is a question-answering system over a personal collection of
papers. Every statement in an answer is linked to the source fragment
it came from, so any claim can be verified against the original text.

## Scope (v0)

**Input:** a local folder with 10-15 PDFs on a single topic, and a
question in natural language.

**Output:** a text answer together with the fragments that support it,
each identified by document and position. If no fragment is relevant
enough, the system states that it cannot answer instead of guessing.

**Interface:** command line, with two operations: index a folder, and ask.

**Explicitly out of scope in v0:** web interface, multiple collections,
conversation memory, cross-document synthesis, summarisation, and any
dedicated vector database.

## Requirements

- Python 3.14.6
- Git

## Installation

```bash
git clone https://github.com/Gjota/escolio.git
cd escolio
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
source .venv/bin/activate       # Linux / macOS
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the required values.

## Usage (planned)

```bash
python -m escolio index ./papers
python -m escolio ask "your question here"
```

## Roadmap

- Evaluation set of 35 questions with a reproducible accuracy score
- Pluggable model providers (local and hosted)
- Multiple collections# escolio


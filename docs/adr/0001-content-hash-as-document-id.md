# 1. Content hash as document identity

## Status
Accepted

## Context
The system indexes a folder of PDFs. Indexing will run several times over
the same folder as documents are added, and each indexed document produces
fragments that are stored and retrieved during queries. Every fragment must
point to its source document so that citations can be verified.

A document therefore needs an identifier, and that choice determines what
happens when indexing runs again.

## Decision
A document is identified by the SHA-256 hash of its bytes, in hexadecimal.

## Alternatives considered
- Random identifier (UUID). This is the standard for entities whose
identity is independent of their content. Here it would produce a new
identifier on every run, so reindexing the same folder would duplicate
every document and its fragments in the index. A single query would then
return the same fragment more than once.

- File path. Stable across runs, but it breaks when the document is moved
or renamed, and it does not detect that two files with different names hold
the same content.

- UUID as primary key, hash as a unique column. This supports versioning
the same document over time. Discarded for now: versioning is out of scope
for v0, and it adds a table and a lookup that no current requirement
justifies.

## Consequences
- Indexing is idempotent: running it twice leaves the system in the same state as running it once. 
Documents already present are detected and skipped.

- Duplicate detection comes for free. Two identical files with different
names produce the same identifier and are indexed only once.

- A document can be moved or renamed without losing its identity.

- Modifying a document, even to fix a typo, produces a different identifier.
The system treats it as a new document, and the previous one remains in the
index with no file backing it. A cleanup mechanism is needed; it is out of
scope for v0.

- Computing the hash requires reading the whole file before deciding whether
to process it. For the expected corpus size this cost is negligible.
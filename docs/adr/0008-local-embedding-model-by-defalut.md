# 8. Local embedding model by default

## Status
Accepted

## Context
Retrieval requires turning both chunks and questions into vectors with the
same model. ADR-0004 requires that model to be multilingual. A monolingual
model would place a question in one language far from a passage that
answers it in another.

The system is meant to work over confidential document collections, and to
be usable by anyone who clones the repository.

Two families are available: models that run locally, and models served over
an API by a third party.

## Decision
The default embedding model is `intfloat/multilingual-e5-small`, run locally
through the `sentence-transformers` library: 384 dimensions, multilingual,
around 470 MB, permissive licence.

It runs in-process rather than behind a local inference server, so cloning
the repository and installing it is enough to index and query.

Hosted models remain a documented option, added once a second provider makes
the differences concrete.

## Alternatives considered
- A hosted embedding API: Generally better retrieval quality and no heavy
dependencies. It requires a key and a payment method, sends the corpus to a
third party, and needs network access. The objection is confidentiality and 
setup, not price.

- A local inference server (Ollama or similar): Loads the model once and
shares it across clients. It requires the user to install and run a separate
service before the project works, and adds an HTTP hop to an operation that
happens in batch during indexing.

- A larger local model (`e5-base`, `bge-m3`): Better benchmark scores at
2 to 5 times the size and the inference cost. The small model is the cheapest
option that satisfies the constraints; growing is a one-line change once
there is a measurement that justifies it.

- A monolingual English model (`all-MiniLM-L6-v2`): The most widely used
option, and the one every tutorial reaches for. Ruled out by ADR-0004.

## Consequences
The corpus never leaves the machine, which is what makes the system usable
over confidential sources. This is a stated property of the project, not an
implementation detail.

Indexing and querying work with no key, no account and no network once the
model is cached.

`sentence-transformers` pulls in PyTorch, which is a heavy dependency for a
project that otherwise has almost none.

E5 models were trained with role prefixes: questions must be prefixed with
`query: ` and chunks with `passage: `. Omitting them degrades retrieval
without any error being raised.

Chunk size is measured with this model's tokeniser. Changing the model may
change what 500 tokens contain.

Replacing the embedding model invalidates every stored vector and requires
reindexing the corpus. The schema records which model produced each vector,
so two models can coexist while a replacement is evaluated.
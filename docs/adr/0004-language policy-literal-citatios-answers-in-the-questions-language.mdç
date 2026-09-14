# 4. Language policy: literal citations, answers in the question's language

## Status
Accepted

## Context
The languages of the corpus and of the question do not necessarily match.
A document may be written in any language, and questions may be asked in
any language.

Two separate pieces of text leave the system on every query: the generated
answer, and the fragments that support it.

Citations exist so that a claim can be checked against the original document.
A citation the user cannot find in the source cannot be checked.

## Alternatives considered
**Translating citations into the language of the question.** Easier to read,
but the translated text does not appear in the source document, so it cannot
be verified against it.

**Answering in the language of the document.** Keeps a single language per
answer. Forces the user to read in a language they did not choose.

**Translating the question before retrieval.** Removes the need for cross-language
retrieval, but adds a model call to the query path, a failure point before retrieval
starts, and loses terminology the user chose deliberately.

## Consequences
The embedding model must be multilingual: a monolingual model places a question and
a relevant passage in different languages far apart. This constrains the choice
recorded in ADR-0005.

Changing the embedding model requires reindexing the whole corpus, since vectors from
different models do not share a vector space.

An answer mixes languages: prose in the question's language, quoted fragments in the
language of each source. The output format has to mark that boundary.

Answer quality depends on reasoning over one language and writing in another.
Part of the evaluation set should ask questions in a language different from the documents.

Optional translation shown alongside the literal citation, never replacing it, is
recorded in the roadmap. It is a service call rather than a computed property: it can
fail and it has a cost.
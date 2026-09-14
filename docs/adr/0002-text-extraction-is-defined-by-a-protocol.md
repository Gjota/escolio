# 2. Text extraction is defined by a Protocol

## Status
Accepted

## Context
Ingestion converts files into text together with their provenance. Only
PDF is supported today, but the corpus may later include plain text, Word
HTML, plus other formats.

The component that orchestrates indexing needs to extract text without
depending on the file format. Otherwise it has to be modified every time a
new format is added.

## Decision
Extraction is defined as a Protocol, "TextExtractor", with a single method
that takes a path and returns the extracted pages. Consuming components
depend on the protocol and receive the concrete implementation from
outside. Only the entry point knows about concrete implementations.

## Alternatives considered
- Calling the concrete function directly. This is the simplest option
and would work today. It forces changes to the orchestrator whenever a
format is added, and it forces tests to use real PDF files or to patch the
module.

- Abstract base class (ABC). This gives the same dependency inversion
and also allows shared code in the base class. It requires every
implementation to inherit from that base, which is not possible when the
implementation comes from an external library. Kept in reserve in case
shared behaviour appears that justifies inheritance.

## Consequences
Adding a new format means writing a class that satisfies the protocol and
registering it at the entry point. No existing component changes.

Tests can use a fake extractor that returns fixed pages, with no files on
disk and no PDF library involved.

Conformance is only checked by a static type checker. At runtime, a class
that does not satisfy the protocol fails only when the missing method is
called.

The protocol fixes the shape of the return value. Changing it requires
modifying every implementation at once.
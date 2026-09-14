# 5. Per-file failures do not stop a folder load

## Status
Accepted

## Context
Indexing runs over a folder of PDFs. A single file may be corrupt,
truncated, password-protected, or otherwise unreadable, and the PDF
library (pypdf) raises a variety of exceptions in those cases.

A folder may hold dozens of documents. The failure of one of them says
nothing about the rest.

## Decision
A failure while loading one document does not stop the folder load. The
result contains both the documents that loaded and the failures, each with
its path and reason. The loader does not report anything to the user: the
caller decides how to surface failures.

## Alternatives considered
- Letting the exception propagate: The caller learns immediately that
something went wrong. One unreadable file out of fifty aborts the whole
run, and the user has to remove it and start over.

- Catching the exception and skipping the file silently: The run always
completes. A document missing from the index is indistinguishable from a
document that was never there, and later answers are built on an
incomplete corpus without anyone knowing.

- Printing a message from inside the loader: Simple, but it ties the
function to a command line. The same function could not be used from a
service or a test without writing to standard output.

## Consequences
A single unreadable file no longer costs a full re-run over the rest of
the corpus.

The loader performs no input or output. The caller decides how to report
failures, which keeps the function usable from a CLI, a service, or a
test.

The catch is deliberately broad. PDF libraries raise a wide and
undocumented range of exceptions on malformed input, and narrowing the
clause would let some of them abort the run. The cost is that a
programming error inside the loader is recorded as a file failure instead
of surfacing. Reviewing the reasons collected in the report is the way to
detect this.

Failures are reported by path and message. Reproducing a failure requires
the original file, which the report does not keep.
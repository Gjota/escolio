# 6. src layout

## Status
Accepted

## Context
The package lived at the repository root. Python resolves imports through
`sys.path`, which includes the directory the interpreter was started from.
Running from the repository root therefore made `import escolio` resolve to
the working copy, whether or not the package was installed.

The project is meant to be installed and eventually deployed, so what is
imported during development should be what is distributed.

## Decision
The `escolio` package lives in `src/escolio`. It is importable only when
installed into the environment, which places `src` on `sys.path` the same
way any third-party library is placed there. Development therefore
requires an editable install.

## Alternatives considered
- Flat layout with an explicit package list: Naming the package in
`pyproject.toml` fixes the build error without moving any file. It does not
fix the underlying problem: the working copy stays importable from the
root, so a packaging mistake still only surfaces on someone else's machine.

- Flat layout relying on automatic discovery: Rejected by setuptools
itself: with `data/` sitting next to the package, it cannot tell which
directories are meant to ship.

## Consequences
A packaging mistake fails locally instead of on a user's machine. A module
left out of the distribution cannot be imported during development either.

Development requires an editable install, which places `src` on `sys.path`
the same way any third-party library is placed there. This is now an
explicit installation step.

Tooling paths change: type checking and tests target `src`. Import
statements are unaffected, since `src` is not part of the package name.


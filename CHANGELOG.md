# Changelog

## Unreleased — 0.3 credibility increment

- Added connected-components checker support across verifier, producer, Python API, and CLI.
- Added exact integer SSSP verification mode (`--exact-int`).
- Added connected-components schema plus valid/tampered examples and malformed/randomized regression tests.
- Added NetworkX end-to-end connected-components integration demo.
- Added reusable GitHub Actions workflow to verify solver-output artifacts in CI.
- Replaced repository owner placeholders and aligned public URLs to `Gianeh/certigraph`.
- Updated docs with connected-components certificate format, proof sketch, and roadmap updates.

## 0.2.0 — GitHub launch kit

- Added launch-ready README, documentation, contribution guide, roadmap, and issue templates.
- Added canonical JSON hashing and lightweight certificate envelopes.
- Added CLI `hash` command.
- Added social preview, logo, architecture diagrams, and terminal demo assets.
- Added randomized regression tests, CLI tests, envelope tests, and malformed-input tests.
- Added JSON Schema drafts for supported certificate formats.
- Added optional NetworkX adapter helpers.

## 0.1.0 — Initial reference artifact

- Added checkers for SSSP, minimum spanning forest, maximum flow/min-cut, topological order, and bipartition.
- Added reference producers, CLI, examples, and initial unit tests.

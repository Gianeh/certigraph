# CertiGraph roadmap

The project’s north star is simple:

> Make result-level verification normal for graph computations.

## 0.2: Launch-ready credibility

- [x] README with a clear narrative and demo.
- [x] CI workflow for Python 3.9–3.13.
- [x] Contribution templates and issue forms.
- [x] Social preview, logo, and explanatory diagrams.
- [x] CLI for verify, produce, and canonical JSON hashing.
- [x] Randomized regression tests.
- [x] JSON Schema drafts.

## 0.3: More graph certificates

High-value checkers:

- strongly connected components + condensation DAG;
- connected components;
- shortest-path tree with exact integer mode;
- bipartite matching + vertex-cover certificate;
- dominator tree certificate;
- Eulerian trail certificate;
- graph coloring checker;
- min-cost flow certificate.

## 0.4: Ecosystem integrations

- NetworkX adapter examples.
- rustworkx adapter.
- OR-Tools flow adapter.
- cuGraph / RAPIDS export checker examples.
- CLI stream mode for pipeline verification.

## 0.5: Hardening

- Full schema versioning policy.
- Fuzzing with Hypothesis and Atheris.
- Exact rational/integer numeric modes.
- Signed certificate envelope examples.
- Benchmark corpus and regression dashboard.

## 1.0: Trusted checker core

A credible 1.0 should have:

- stable public API;
- stable certificate schemas;
- high coverage and fuzzing;
- formal proof plan for the core checkers;
- a language-portability plan, likely Rust/WASM for browser and pipeline use.

## Moonshots

- Proof-carrying NetworkX: wrappers that return certificates by default.
- “Verify this solver output” GitHub Action.
- Browser playground for graph certificates.
- Formalized CertiGraph Core in Lean/Coq/Isabelle.
- A benchmark suite of adversarial graph certificates.

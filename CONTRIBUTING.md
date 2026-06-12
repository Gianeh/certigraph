# Contributing to CertiGraph

CertiGraph needs contributors who care about a deceptively simple contract:

> A producer may be complicated. A checker must stay small enough to distrust productively.

This guide is optimized for useful, reviewable contributions.

## Fast setup

```bash
git clone https://github.com/YOUR_ORG/certigraph.git
cd certigraph
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .[dev]
make test
```

The runtime package has zero dependencies. Development tools are optional.

## Contribution lanes

### 1. Add a checker

A good CertiGraph checker has:

- a clear certificate format;
- a concise proof sketch;
- deterministic failure messages;
- no dependency on the producer implementation;
- tests that show both acceptance and rejection;
- at least one tampered certificate example.

Recommended file set:

```text
certigraph/verify.py                  checker function
certigraph/produce.py helper           optional reference producer
schemas/<problem>.certificate.schema.json
tests/test_<problem>.py
examples/<problem>_valid.json
examples/invalid/<problem>_tampered.json
docs/certificate-formats.md            format docs update
docs/research.md                       proof sketch update
```

Checker API shape:

```python
def check_problem_certificate(instance, claimed_output, certificate, *, abs_tol: float = 1e-9) -> CheckResult:
    ...
```

Return `CheckResult`; do not raise for malformed certificates unless the caller passed objects outside the documented Python API contract.

### 2. Add integrations

Optional integrations belong in `certigraph/adapters/` and must degrade gracefully when the third-party package is not installed. Import heavy libraries inside functions or behind clear optional paths.

### 3. Improve testing

Especially valuable:

- randomized tests with deterministic seeds;
- brute-force cross-checks on tiny instances;
- malformed inputs that should return clean rejections;
- large sparse examples for performance regressions;
- exact arithmetic experiments for adversarial numerical cases.

### 4. Improve docs and launch material

Great docs are part of the product. Useful PRs include diagrams, examples from real domains, comparison tables, or short “why this matters” explanations.

## Review checklist for checker PRs

Before requesting review, answer these in the PR description:

1. What mathematical theorem makes the certificate sufficient?
2. Is the checker independent from the producer?
3. What is the trusted computing base added by this PR?
4. What malformed or adversarial cases are tested?
5. What is the asymptotic cost of verification?
6. What numerical assumptions are required?

## Style

- Keep checker code boring.
- Prefer explicit validation over clever Python tricks.
- Use precise failure messages; they are part of the UX.
- Keep examples small enough to understand in a README.
- Avoid adding runtime dependencies unless the project has no viable alternative.

## Running checks

```bash
make test
make coverage
make lint
make typecheck
```

`make ci` runs the full local suite.

## Good first issues

Good first contributions are usually one of:

- a new invalid certificate example;
- a small domain demo;
- a JSON Schema improvement;
- a clearer failure message;
- a doc diagram;
- a brute-force oracle for tiny graphs.

## Maintainer expectations

CertiGraph should be welcoming, rigorous, and intellectually honest. Bugs in checkers matter more than feature velocity. A small verified core is more valuable than a large magical API.

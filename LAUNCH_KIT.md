# CertiGraph launch kit

This is the practical playbook for turning CertiGraph from “nice artifact” into a repository people understand, star, use, and contribute to.

## Positioning

Do **not** position CertiGraph as another graph library.

Position it as:

> A tiny verification layer for graph results produced by untrusted, optimized, remote, distributed, or AI-generated solvers.

The emotional hook is trust. The technical hook is proof-carrying results.

## Repository setup checklist

Before public launch:

- [ ] Replace every `YOUR_ORG` placeholder.
- [ ] Create labels: `checker`, `good first issue`, `proof-sketch`, `security`, `demo`, `docs`, `needs-triage`, `design-needed`.
- [ ] Upload `docs/assets/social-preview.png` in GitHub repository settings as the social preview.
- [ ] Add topics: `certifying-algorithms`, `graph-algorithms`, `verifiable-computation`, `proof-carrying-data`, `python`, `networkx`, `algorithms`.
- [ ] Enable Discussions with categories: Ideas, Show and tell, Checker proposals, Q&A.
- [ ] Pin these issues:
  - “Add bipartite matching checker.”
  - “Port one checker to Rust/WASM.”
  - “Add Hypothesis fuzzing for malformed certificates.”
  - “Build a browser playground.”
- [ ] Publish v0.2.0 release notes using `CHANGELOG.md`.
- [ ] Enable GitHub Pages using the Docs workflow.
- [ ] Add the package to PyPI once the name is available.

## Launch narrative

### One-liner

CertiGraph lets untrusted and AI-generated graph solvers return proof-carrying results that a tiny Python checker can verify.

### Slightly longer

Graph algorithms are everywhere, but modern graph results increasingly come from systems we cannot or do not want to inspect: AI agents, remote solvers, distributed jobs, GPU kernels, vendor APIs. CertiGraph makes those results carry a small certificate, so downstream systems can verify correctness before acting.

### Technical positioning

CertiGraph implements certifying algorithms for graph problems: shortest paths, MST/MSF, max-flow/min-cut, topological order, and bipartition. Producers can be complex; checkers stay small, deterministic, and dependency-free.

## GitHub repository description

> Proof-carrying graph results: tiny independent checkers for untrusted and AI-generated solvers.

## Suggested README social card text

> Do not trust the solver. Verify the result.


## Video demo assets

Use these assets in the public launch:

- README teaser: `docs/assets/certigraph-demo-teaser.gif`
- Full demo: `docs/assets/certigraph-demo.mp4`
- Upload captions: `docs/assets/certigraph-demo.srt`
- Thumbnail/poster: `docs/assets/certigraph-demo-thumbnail.png`

Suggested caption for video posts:

> I built CertiGraph: proof-carrying graph results for untrusted and AI-generated solvers. Here is the whole idea in 57 seconds: the wrong answer gets rejected; the proof-carrying answer gets verified.

## Launch posts

### Hacker News title options

- Show HN: CertiGraph – proof-carrying graph results for untrusted solvers
- Show HN: I built a tiny checker layer for AI-generated graph algorithms
- Show HN: Certifying graph results instead of trusting graph solvers

HN body:

> I built CertiGraph, a small dependency-free Python toolkit for proof-carrying graph results. The idea is that an algorithm returns not only an answer, but also a certificate that a small independent checker can validate.
>
> Current checkers cover shortest paths, minimum spanning forest, max-flow/min-cut, topological order, and bipartition. The motivating use case is verifying outputs from untrusted, optimized, distributed, or AI-generated solvers.
>
> The project is alpha, but the core pattern is useful: producers can be complicated; checkers should be boring.

### X / Twitter

> I made CertiGraph: proof-carrying graph results for untrusted and AI-generated solvers.
>
> The solver can be huge, remote, optimized, or LLM-written. The result carries a certificate. A tiny dependency-free Python checker accepts or rejects it.
>
> Do not trust the solver. Verify the result.

### LinkedIn

> Modern software increasingly relies on computational results from systems we cannot easily audit: AI agents, distributed workflows, optimization services, and high-performance native code.
>
> I launched CertiGraph, a small Python toolkit for proof-carrying graph results. It implements independent checkers for shortest paths, MST/MSF, max-flow/min-cut, topological order, and bipartition.
>
> The principle is simple: let complex systems produce results, but require those results to carry evidence that a small checker can verify.

### Reddit / technical communities

> CertiGraph is a tiny dependency-free Python package for certifying graph results. It is inspired by certifying algorithms and proof-carrying code/data. I’d especially appreciate feedback on certificate formats, checker APIs, and which graph certificate should come next.

## First “good issues” to create

### Add a bipartite matching checker

Certificate: matching edges plus a vertex cover. Verification: matching feasibility, cover feasibility, and equal cardinality by König’s theorem.

### Add SCC condensation checker

Certificate: component id per vertex plus condensation topological order. Verification: every SCC is strongly connected, no merged components are mutually reachable, condensation edges go forward.

### Add exact integer mode for SSSP

Current numeric checks use finite Python numbers and absolute tolerance. Exact integer mode should reject floats and avoid tolerance entirely.

### Add a Rust/WASM topological-order checker

A tiny WASM checker would enable browser verification demos and workflow-engine integrations.

### Add certificate corpus

Collect small real-world graph examples: build dependencies, package managers, network routing, supply chain flow, compiler passes, and data pipeline DAGs.

## Demo script for a short video

1. Show a bad AI-generated shortest-path result.
2. Run `python examples/ai_solver_wrong_answer_demo.py`.
3. Highlight the rejection message.
4. Produce a valid certificate.
5. Run the verifier successfully.
6. End with: “Do not trust the solver. Verify the result.”

## Metrics that matter

Stars are useful, but the better signals are:

- external demos using CertiGraph;
- new checker proposals;
- checker bug reports;
- integrations with existing graph packages;
- formal verification attempts;
- citations in teaching material.

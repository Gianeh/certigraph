# Concepts

## Producer

The producer computes a result and emits a certificate. It may be optimized, distributed, stochastic, remote, or untrusted.

Examples:

- a NetworkX script;
- a Rust service;
- a GPU solver;
- a workflow engine;
- an LLM-generated algorithm;
- a vendor optimization API.

## Checker

The checker validates the result and certificate. It should be:

- small;
- deterministic;
- independent from the producer;
- explicit about numeric assumptions;
- easy to audit;
- easy to fuzz;
- eventually formally verifiable.

## Certificate

A certificate is evidence that a particular result is correct for a particular instance.

For shortest paths, the certificate is a parent edge for each reachable vertex. For max flow, it is a feasible flow and an s-t cut of the same value. Different problems need different witnesses.

## Trusted computing base

The trusted computing base is the code you still have to trust. CertiGraph tries to keep it small by moving complexity into untrusted producers and keeping verification boring.

## What CertiGraph does not do yet

CertiGraph does not yet provide cryptographic signatures, formal proofs of checker implementations, or hardened parsing for adversarial deployments. The envelope helpers provide canonical hashes, but signing should be layered on top with tools such as Sigstore, GPG, minisign, or an organization-specific transparency log.

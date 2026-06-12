# Checker design

CertiGraph checkers follow a few rules.

## Keep the checker independent

A checker should not call the producer, reuse the producer’s internal state, or depend on a heavy graph library to decide correctness.

Reference producers are allowed for demos and tests, but verification must stand alone.

## Return structured results

Checkers return `CheckResult`:

```python
@dataclass(frozen=True)
class CheckResult:
    ok: bool
    message: str
    details: dict[str, object]
```

This makes CLI output, logs, dashboards, and tests easier to build.

## Fail specifically

A useful checker tells you *why* it rejected a certificate. Prefer:

```text
edge relaxation would improve claimed distance
```

over:

```text
invalid
```

## Validate before proving

The usual checker structure is:

1. validate vertices and edge endpoints;
2. parse certificate fields;
3. check local feasibility constraints;
4. check global optimality witness;
5. return acceptance with small metadata.

## Separate numerical policy

Most current checkers use finite Python numbers and an absolute tolerance. For adversarial settings, exact integer/rational modes should be preferred.

## Add tampering tests

For every valid example, create at least one invalid variant that changes a plausible-looking field. A good checker should reject the altered certificate with a meaningful message.

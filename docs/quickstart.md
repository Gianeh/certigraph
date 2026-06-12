# Quickstart

## Install

From PyPI after the first package release:

```bash
pip install certigraph
```

For local development:

```bash
git clone https://github.com/YOUR_ORG/certigraph.git
cd certigraph
python -m pip install -e .[dev]
python -m unittest discover -v
```

## Verify a certificate

From a repository clone:

```bash
python -m certigraph verify sssp examples/sssp_valid.json
```

The CLI exits with:

- `0` if the certificate is accepted;
- `2` if the certificate is rejected;
- `1` for malformed CLI usage or unexpected boundary errors.

## Produce then verify

Reference producers are included for examples and tests:

```bash
python -m certigraph produce msf examples/msf_graph_only.json --out /tmp/msf.cert.json
python -m certigraph verify msf /tmp/msf.cert.json
```

The producer is not trusted. It is just a convenient way to generate examples.

## Hash a certificate

```bash
python -m certigraph hash examples/sssp_valid.json
python -m certigraph hash examples/sssp_valid.json --envelope-kind sssp
```

Use the hash in build logs, workflow artifacts, or audit trails.

## Python API

```python
from certigraph import check_topological_order

vertices = ["parse", "typecheck", "optimize", "emit"]
edges = [("parse", "typecheck"), ("typecheck", "optimize"), ("optimize", "emit")]
order = ["parse", "typecheck", "optimize", "emit"]

result = check_topological_order(vertices, edges, order)
assert result.ok, result.message
```

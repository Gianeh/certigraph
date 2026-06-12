# Benchmark notes

Run locally with:

```bash
python benchmarks/benchmark_checkers.py
```

This benchmark is intentionally dependency-free and should be treated as a smoke test rather than a publication-quality benchmark. The main question is whether checker runtime stays comfortably smaller and simpler than typical producer runtime.

When publishing benchmark numbers, include:

- CPU model;
- Python version;
- graph sizes;
- whether weights/capacities are integers or floats;
- exact command used.

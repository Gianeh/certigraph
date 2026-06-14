# Certificate formats

The CLI uses JSON. Python APIs accept ordinary Python containers.

## Single-source shortest paths

```json
{
  "vertices": ["s", "a", "b"],
  "source": "s",
  "edges": [
    {"u": "s", "v": "a", "w": 2},
    {"u": "a", "v": "b", "w": -1}
  ],
  "distance": {"s": 0, "a": 2, "b": 1},
  "parent": {
    "s": null,
    "a": {"u": "s", "edge": 0},
    "b": {"u": "a", "edge": 1}
  }
}
```

Use `null`, `"inf"`, or `"unreachable"` for unreachable vertices.

For integer-only certificates, run:

```bash
python -m certigraph verify sssp artifact.json --exact-int --abs-tol 0
```

In exact mode, all finite edge weights and distances must be integers.

## Minimum spanning forest

```json
{
  "vertices": ["a", "b", "c"],
  "edges": [
    {"u": "a", "v": "b", "w": 1},
    {"u": "b", "v": "c", "w": 2},
    {"u": "a", "v": "c", "w": 5}
  ],
  "chosen": [0, 1]
}
```

`chosen` contains edge indices.

## Maximum flow

```json
{
  "vertices": ["s", "a", "b", "t"],
  "source": "s",
  "sink": "t",
  "edges": [
    {"u": "s", "v": "a", "capacity": 3},
    {"u": "s", "v": "b", "capacity": 2},
    {"u": "a", "v": "t", "capacity": 2},
    {"u": "b", "v": "t", "capacity": 3},
    {"u": "a", "v": "b", "capacity": 1}
  ],
  "flow": [3, 2, 2, 3, 1],
  "cut": ["s"]
}
```

`flow[i]` is the flow on edge `i`. `cut` is the source side of an s-t cut.

## Topological order

```json
{
  "vertices": ["parse", "typecheck", "emit"],
  "edges": [
    {"u": "parse", "v": "typecheck"},
    {"u": "typecheck", "v": "emit"}
  ],
  "order": ["parse", "typecheck", "emit"]
}
```

## Bipartition

```json
{
  "vertices": ["u1", "u2", "v1"],
  "edges": [
    {"u": "u1", "v": "v1"},
    {"u": "u2", "v": "v1"}
  ],
  "color": {"u1": 0, "u2": 0, "v1": 1}
}
```

Color values are arbitrary; only equality and inequality matter.

## Connected components

```json
{
  "vertices": ["a", "b", "c", "d", "e", "f"],
  "edges": [
    {"u": "a", "v": "b"},
    {"u": "b", "v": "c"},
    {"u": "d", "v": "e"}
  ],
  "component": {"a": 0, "b": 0, "c": 0, "d": 1, "e": 1, "f": 2}
}
```

Acceptance criteria:

- every vertex has a component label;
- every edge stays within one claimed label;
- labels neither split a true connected component nor merge disconnected components.

Rejection examples:

- edge endpoints with different labels;
- missing component labels;
- two disconnected components sharing the same label.

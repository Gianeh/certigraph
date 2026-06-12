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
